/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { AccountReport } from "@account_reports/components/account_report/account_report";
import { rpc } from "@web/core/network/rpc";

patch(AccountReport.prototype, {
    setup() {
        super.setup();
        if (this.props?.action?.xml_id === "account_reports.action_account_report_partner_ledger") {
            setTimeout(() => this._addInitialBalanceBtn(), 1500);
        }
    },

    /* ---------- UI ---------- */
    _addInitialBalanceBtn() {
        const panel = document.querySelector('.o_control_panel');
        if (!panel || document.querySelector('#show_initial_balance_btn')) return;

        const refBtn = document.querySelector('#filter_rounding_unit');
        if (!refBtn) return;

        const btn = document.createElement('button');
        btn.id        = 'show_initial_balance_btn';
        btn.className = 'btn btn-secondary';
        btn.innerHTML = '<i class="fa fa-columns me-1"></i>Initial Balance';
        btn.onclick   = () => this._toggleColumn();
        refBtn.parentNode.insertBefore(btn, refBtn);
    },

    _toggleColumn() {
        const btn = document.querySelector('#show_initial_balance_btn');
        const col = document.querySelector('.initial-balance-column');
        if (col) {
            document.querySelectorAll('.initial-balance-column').forEach(el => el.remove());
            btn.className = 'btn btn-secondary';
            btn.innerHTML = '<i class="fa fa-columns me-1"></i>Initial Balance';
        } else {
            this._showColumn();
            btn.className = 'btn btn-success';
            btn.innerHTML = '<i class="fa fa-columns me-1"></i>Initial Balance ✓';
        }
    },

    async _showColumn() {
        this._addHeader();
        let balances = {};
        try {
            const opts = this.props?.context?.options || {};
            balances = await rpc("/web/dataset/call_kw", {
                model:  "account.partner.ledger.report.handler",
                method: "get_partner_initial_balances",
                args:   [opts],
                kwargs: {}
            });
        } catch (e) {
            console.error("RPC opening balance error:", e);
        }
        this._fillCells(balances || {});
    },

    /* ---------- table helpers ---------- */
    _addHeader() {
        const row = document.querySelector('thead tr:nth-child(2)') || document.querySelector('thead tr');
        if (!row || row.querySelector('.initial-balance-column')) return;

        const balanceTh = row.querySelector('[data-expression_label="balance"]');
        if (!balanceTh) return;

        const th = document.createElement('th');
        th.className        = 'initial-balance-column';
        th.style.textAlign  = 'right';
        th.textContent      = 'Initial Balance';
        balanceTh.parentNode.insertBefore(th, balanceTh);
    },

    _fillCells(balances) {
        const rows = document.querySelectorAll('tbody tr');
        let isLastRow = false;

        rows.forEach((tr, index) => {
            if (tr.querySelector('.initial-balance-column')) return;

            const balanceTd = tr.querySelector('[data-expression_label="balance"]');
            if (!balanceTd) return;

            // Check if this is the last row (total row)
            isLastRow = (index === rows.length - 1) ||
                       tr.classList.contains('o_account_reports_total_line') ||
                       tr.querySelector('.o_account_reports_total_line') ||
                       tr.style.fontWeight === 'bold';

            let val;
            if (isLastRow && balances.total !== undefined) {
                // This is the total row, show the total
                val = this._formatBalance(balances.total);
            } else {
                // Regular partner row
                const partnerName = this._getPartnerName(tr);
                val = partnerName && balances[partnerName] ? balances[partnerName] : '0.00 LE';
            }

            const td = document.createElement('td');
            td.className = 'initial-balance-column numeric text-end';
            td.style.textAlign = 'right';

            // Make total row bold
            if (isLastRow) {
                td.style.fontWeight = 'bold';
            }

            td.innerHTML = `<div class="wrapper"><div class="content"><div class="name">${val}</div></div></div>`;
            balanceTd.parentNode.insertBefore(td, balanceTd);
        });
    },

    // Helper method to format balance
    _formatBalance(amount) {
        if (amount === 0) return "0.00 LE";

        const formatted = Math.abs(amount).toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }) + " LE";

        return amount >= 0 ? formatted : `(${formatted})`;
    },

    _getPartnerName(tr) {
        const cell = tr.querySelector('[data-id="line_name"] .name') || tr.querySelector('.o_account_report_line_name');
        return cell ? cell.textContent.trim() : '';
    }
});
