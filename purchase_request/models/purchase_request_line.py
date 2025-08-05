from odoo import models, fields, api

class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    product_id = fields.Many2one('product.product', required=True)
    description = fields.Char(compute='_set_description', store=True)
    request_id = fields.Many2one('purchase.request')
    quantity = fields.Float(default=1)
    total = fields.Float(compute='_compute_total', store=True)
    cost_price = fields.Float(string="Cost Price", readonly=True, compute='_set_cost_price', store=True)

    @api.depends('quantity', 'cost_price')
    def _compute_total(self):
        """
        Compute the total amount for this request line.
        """
        for rec in self:
            rec.total = rec.quantity * rec.cost_price

    @api.depends('product_id')
    def _set_description(self):
        """
        Set the description based on selected product.
        """
        for line in self:
            line.description = line.product_id.name or ''

    @api.depends('product_id')
    def _set_cost_price(self):
        """
        Set the cost price from the product.
        """
        for line in self:
            line.cost_price = line.product_id.standard_price or 0.0
