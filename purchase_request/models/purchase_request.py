from odoo import models, fields, api

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'

    name = fields.Char(required=True, string='Request Name')
    is_editable = fields.Boolean(
        string='Is Editable',
        compute='_compute_is_editable',
        store=True,
        readonly=True
    )
    requested_by = fields.Many2one('res.users',
                                   string='Request by',
                                   default=lambda self: self.env.user)
    start_date = fields.Date(default=fields.Date.today)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approve', 'Approve'),
        ('to_be_approve', 'To Be Approve'),
        ('reject', 'Reject'),
        ('cancel', 'Cancel'),
    ], default='draft')
    end_date = fields.Date()
    total_price = fields.Float(compute='_compute_total_price')
    reason = fields.Text(string='Rejection Reason', readonly=True)
    order_lines_ids = fields.One2many('purchase.request.line', 'request_id')

    @api.depends('status')
    def _compute_is_editable(self):
        """
        Compute whether the request is editable or not depending on the status.
        """
        for rec in self:
            rec.is_editable = rec.status in ('draft', 'to_be_approve')

    def action_submit_for_approval(self):
        """
        Submit the purchase request for approval.
        """
        for rec in self:
            rec.status = 'to_be_approve'

    def action_approve(self):
        """
        Approve the purchase request, disable editing, and notify managers by email.
        """
        for rec in self:
            rec.status = 'approve'
            purchase_manager_group = self.env.ref('purchase.group_purchase_manager')
            users = purchase_manager_group.users
            subject = f"Purchase Request ({rec.name}) has been approved"
            body = f"<p>The purchase request <strong>{rec.name}</strong> has been approved.</p>"

            for user in users:
                if user.partner_id.email:
                    self.env['mail.mail'].create({
                        'subject': subject,
                        'body_html': body,
                        'email_to': user.partner_id.email,
                    }).send()

    def action_reject(self):
        """
        Mark the purchase request as rejected and open the rejection reason wizard.
        """
        for rec in self:
            rec.status = 'reject'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'rejection.reason',
            'view_mode': 'form',
            'view_id': self.env.ref('purchase_request.rejection_reason_wizard_view_form').id,
            'target': 'new',
            'context': {
                'default_request_id': self.id,
            }
        }

    def action_reset_to_draft(self):
        """
        Reset the status to draft to allow editing.
        """
        for rec in self:
            rec.status = 'draft'

    def action_cancel_request(self):
        """
        Cancel the purchase request and allow editing (if needed).
        """
        for rec in self:
            rec.status = 'cancel'

    @api.depends('order_lines_ids.total')
    def _compute_total_price(self):
        """
        Compute the total price for all order lines.
        """
        for record in self:
            record.total_price = sum(line.total for line in record.order_lines_ids)
