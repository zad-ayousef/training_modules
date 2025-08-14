from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def compute_initial_balance(self, date_from=None):
        """Compute initial balance for this partner before a specific date"""
        if not date_from:
            date_from = fields.Date.today().replace(month=1, day=1)

        domain = [
            ('partner_id', '=', self.id),
            ('date', '<', date_from),
            ('move_id.state', '=', 'posted'),
            ('account_id.account_type', 'in', ['asset_receivable', 'liability_payable'])
        ]

        move_lines = self.env['account.move.line'].search(domain)
        return sum(move_lines.mapped('balance'))


class AccountPartnerLedgerReportHandler(models.AbstractModel):
    _inherit = "account.partner.ledger.report.handler"

    @api.model
    def get_partner_initial_balances(self, options):
        """RPC method to get initial balances for partners"""
        try:
            date_from = options.get('date', {}).get('date_from')
            if not date_from:
                date_from = fields.Date.today().replace(month=1, day=1)
            elif isinstance(date_from, str):
                date_from = fields.Date.from_string(date_from)

            partner_ids = self._get_report_partner_ids()

            result = {}
            for partner_id in partner_ids:
                partner = self.env['res.partner'].browse(partner_id)
                if partner.exists():
                    initial_balance = partner.compute_initial_balance(date_from)
                    result[partner.name] = self._format_currency(initial_balance)

            return result

        except Exception:
            return {}

    def _get_report_partner_ids(self):
        """Get partner IDs that have transactions"""
        domain = [
            ('partner_id', '!=', False),
            ('account_id.account_type', 'in', ['asset_receivable', 'liability_payable'])
        ]

        move_lines = self.env['account.move.line'].search(domain, limit=1000)
        return list(set(move_lines.mapped('partner_id').ids))

    def _format_currency(self, amount):
        """Format amount for display"""
        if amount == 0:
            return "0.00 LE"

        formatted = "{:,.2f} LE".format(abs(amount))
        if amount < 0:
            formatted = f"({formatted})"
        return formatted
