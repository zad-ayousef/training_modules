from odoo import models, fields, api


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Online Course'

    name = fields.Char(required=True, string='Request Name')
    is_editable = fields.Boolean(default=1)
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

    def action_submit_for_approval(self):
        for rec in self:
            rec.status = 'to_be_approve'

    def action_approve(self):
        for rec in self:
            rec.status = 'approve'
            rec.is_editable = False

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

    # def action_approve(self):
    #     for rec in self:
    #         rec.status = 'approve'
    #         rec.is_editable = 0

    def action_reject(self):
        for rec in self:
            rec.status = 'reject'
            rec.is_editable = 0
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
        for rec in self:
            rec.status = 'draft'
            rec.is_editable = 1

    def action_cancel_request(self):
        for rec in self:
            rec.status = 'cancel'
            rec.is_editable = 1

    @api.depends('order_lines_ids.total')
    def _compute_total_price(self):
        for record in self:
            record.total_price = sum(line.total for line in record.order_lines_ids)


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'

    product_id = fields.Many2one('product.product', required=True)

    description = fields.Char(compute='set_description', store=1)

    request_id = fields.Many2one('purchase.request')

    quantity = fields.Float(default=1)
    total = fields.Float(compute='compute_total', store=True)
    cost_price = fields.Float(string="Cost Price", readonly=True, compute='set_cost_price', store=True)

    @api.depends('quantity', 'cost_price')
    def compute_total(self):
        for rec in self:
            rec.total = (rec.quantity * rec.cost_price)

    @api.depends('product_id')
    def set_description(self):
        for line in self:
            line.description = line.product_id.name or ''

    @api.depends('product_id')
    def set_cost_price(self):
        for line in self:
            line.cost_price = line.product_id.standard_price or 0.0
