from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def get_opening_balance(self):
        total = 0.0

        if self.property_account_receivable_id:
            total += self.property_account_receivable_id.opening_balance or 0.0

        if (self.property_account_payable_id and
                self.property_account_payable_id != self.property_account_receivable_id):
            total += self.property_account_payable_id.opening_balance or 0.0

        return total


class AccountPartnerLedgerReportHandler(models.AbstractModel):
    _inherit = "account.partner.ledger.report.handler"

    @api.model
    def get_partner_initial_balances(self, options):
        try:
            partners = self._get_report_partners(options)

            result = {}
            total_balance = 0.0

            for partner in partners:
                opening_balance = partner.get_opening_balance()
                result[partner.name] = self._format_balance(opening_balance)
                total_balance += opening_balance

            # Include the total as a separate key
            result['total'] = total_balance

            return result

        except Exception as e:
            return {"error": f"Error getting opening balances: {str(e)}"}

    def _get_report_partners(self, options):
        domain = [
            ('partner_id', '!=', False),
            ('account_id.account_type', 'in', ['asset_receivable', 'liability_payable']),
            ('move_id.state', '=', 'posted')
        ]

        if options and options.get('date'):
            date_filters = options['date']
            if date_filters.get('date_from'):
                domain.append(('date', '>=', date_filters['date_from']))
            if date_filters.get('date_to'):
                domain.append(('date', '<=', date_filters['date_to']))

        move_lines = self.env['account.move.line'].search(domain)
        partner_ids = list(set(move_lines.mapped('partner_id.id')))

        return self.env['res.partner'].browse(partner_ids)

    def _format_balance(self, amount):
        if amount == 0:
            return "0.00 LE"

        formatted = "{:,.2f} LE".format(abs(amount))
        return formatted if amount >= 0 else f"({formatted})"
