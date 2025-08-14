/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { AccountReport } from "@account_reports/components/account_report/account_report";
import { rpc } from "@web/core/network/rpc";

patch(AccountReport.prototype, {
    setup() {
        super.setup();
        if (this.props?.action?.xml_id === "account_reports.action_account_report_partner_ledger") {
            setTimeout(() => this._addShowInitialBalanceButton(), 2000);
        }
    },

    _addShowInitialBalanceButton() {
        const controlPanel = document.querySelector('.o_control_panel');

        if (controlPanel && !document.querySelector('#show_initial_balance_btn')) {
            const reportButton = document.querySelector('#filter_variant');
            const currencyButton = document.querySelector('#filter_rounding_unit');

            if (reportButton && currencyButton) {
                const buttonContainer = document.createElement('div');
                buttonContainer.id = 'filter_initial_balance';

                const showButton = document.createElement('button');
                showButton.id = 'show_initial_balance_btn';
                showButton.type = 'button';
                showButton.className = 'btn btn-secondary';
                showButton.title = 'Toggle Initial Balance column visibility';
                showButton.innerHTML = '<i class="fa fa-columns me-1"></i>Show Initial Balance';

                showButton.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this._toggleInitialBalanceColumn();
                });

                buttonContainer.appendChild(showButton);
                currencyButton.parentNode.insertBefore(buttonContainer, currencyButton);
            }
        }
    },

    _toggleInitialBalanceColumn() {
        const button = document.querySelector('#show_initial_balance_btn');
        const table = document.querySelector('.o_account_reports_table, table');

        if (!table) {
            console.log("Table not found");
            return;
        }

        const isColumnVisible = table.querySelector('.initial-balance-column');

        if (isColumnVisible) {
            this._hideInitialBalanceColumn();
            button.className = 'btn btn-secondary';
            button.innerHTML = '<i class="fa fa-columns me-1"></i>Show Initial Balance';
        } else {
            this._showInitialBalanceColumn();
            button.className = 'btn btn-success';
            button.innerHTML = '<i class="fa fa-columns me-1"></i>Show Initial Balance ✓';
        }
    },

    async _showInitialBalanceColumn() {
        const table = document.querySelector('.o_account_reports_table, table');
        if (!table) return;

        // Add header
        this._addColumnHeader();

        // Get data from Python backend
        try {
            const options = this._getCurrentOptions();
            const partnerBalances = await rpc("/web/dataset/call_kw", {
                model: "account.partner.ledger.report.handler",
                method: "get_partner_initial_balances",
                args: [options],
                kwargs: {}
            });

            this._addDataCellsWithRealValues(partnerBalances);

        } catch (error) {
            console.error("Failed to get initial balance data from Python:", error);
            this._addDataCellsWithFallbackData();
        }
    },

    _addColumnHeader() {
        const table = document.querySelector('.o_account_reports_table, table');
        const headerRows = table.querySelectorAll('thead tr');

        if (headerRows.length >= 2) {
            const columnHeaderRow = headerRows[1];
            const headers = columnHeaderRow.querySelectorAll('th');
            let balanceHeaderIndex = -1;

            headers.forEach((header, index) => {
                const expressionLabel = header.getAttribute('data-expression_label');
                if (expressionLabel === 'balance') {
                    balanceHeaderIndex = index;
                }
            });

            if (balanceHeaderIndex >= 0) {
                const balanceHeader = headers[balanceHeaderIndex];
                const newHeader = document.createElement('th');

                newHeader.setAttribute('colspan', '1');
                newHeader.setAttribute('data-expression_label', 'initial_balance');
                newHeader.className = 'initial-balance-column';
                newHeader.style.textAlign = 'right';
                newHeader.style.whiteSpace = 'nowrap';
                newHeader.textContent = 'Initial Balance';

                balanceHeader.parentNode.insertBefore(newHeader, balanceHeader);
            }
        }
    },

    _getCurrentOptions() {
        let options = {};

        try {
            if (this.props && this.props.context && this.props.context.options) {
                options = { ...this.props.context.options };
            } else {
                const currentDate = new Date();
                const yearStart = new Date(currentDate.getFullYear(), 0, 1);

                options = {
                    date: {
                        date_from: yearStart.toISOString().split('T')[0],
                        date_to: currentDate.toISOString().split('T')[0]
                    },
                    show_initial_balance: true
                };
            }
        } catch (e) {
            options = {
                date: {
                    date_from: new Date().getFullYear() + '-01-01',
                    date_to: new Date().toISOString().split('T')[0]
                },
                show_initial_balance: true
            };
        }

        return options;
    },

    _addDataCellsWithRealValues(partnerBalances) {
        const table = document.querySelector('.o_account_reports_table, table');
        if (!table) return;

        const dataRows = table.querySelectorAll('tbody tr');
        dataRows.forEach(row => {
            if (row.querySelector('.initial-balance-column')) {
                return;
            }

            this._createInitialBalanceCell(row, partnerBalances);
        });
    },

    _addDataCellsWithFallbackData() {
        const table = document.querySelector('.o_account_reports_table, table');
        if (!table) return;

        const dataRows = table.querySelectorAll('tbody tr');
        dataRows.forEach(row => {
            if (row.querySelector('.initial-balance-column')) {
                return;
            }

            this._createInitialBalanceCell(row, {});
        });
    },

    _createInitialBalanceCell(row, partnerBalances) {
        const cells = row.querySelectorAll('td');
        let balanceCellIndex = -1;

        cells.forEach((cell, index) => {
            const expressionLabel = cell.getAttribute('data-expression_label');
            if (expressionLabel === 'balance') {
                balanceCellIndex = index;
            }
        });

        if (balanceCellIndex >= 0) {
            const balanceCell = cells[balanceCellIndex];
            const newCell = document.createElement('td');

            newCell.className = 'line_cell numeric text-end initial-balance-column';
            newCell.style.textAlign = 'right';
            newCell.style.whiteSpace = 'nowrap';
            newCell.style.padding = '8px';

            const wrapper = document.createElement('div');
            wrapper.className = 'wrapper';
            const content = document.createElement('div');
            content.className = 'content';
            const nameDiv = document.createElement('div');
            nameDiv.className = 'name';

            // Get initial balance value (simplified)
            const partnerName = this._getPartnerNameFromRow(row);
            let initialBalance = '0.00 LE';

            if (partnerBalances && Object.keys(partnerBalances).length > 0 && partnerBalances[partnerName]) {
                initialBalance = partnerBalances[partnerName];
            }
            // Removed fallback calculation - always shows 0.00 LE if no Python data

            nameDiv.textContent = initialBalance;

            content.appendChild(nameDiv);
            wrapper.appendChild(content);
            newCell.appendChild(wrapper);

            balanceCell.parentNode.insertBefore(newCell, balanceCell);
        }
    },

    _getPartnerNameFromRow(row) {
        const nameCell = row.querySelector('[data-id="line_name"] .name');
        return nameCell ? nameCell.textContent.trim() : '';
    },

    _hideInitialBalanceColumn() {
        const columns = document.querySelectorAll('.initial-balance-column');
        columns.forEach(column => column.remove());
    }
});
