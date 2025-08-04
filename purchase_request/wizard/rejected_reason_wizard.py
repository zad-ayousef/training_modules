from odoo import fields, models


class RejectionReason(models.TransientModel):
    _name = 'rejection.reason'

    request_id = fields.Many2one('purchase.request')
    rejection_reason = fields.Text(string='Rejection Reason', required=True)

    def action_confirm(self):
        self.request_id.write({
            'reason': self.rejection_reason,
        })
