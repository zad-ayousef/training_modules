from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount_amount = fields.Monetary(
        string='Discount Amount',
        compute='_compute_discount_amount',
        store=True,
        currency_field='currency_id',
    )

    @api.depends('product_qty', 'price_unit', 'price_subtotal', 'discount')
    def _compute_discount_amount(self):
        for line in self:
            if line.discount > 0 and line.price_unit > 0 and line.product_qty > 0:
                line.discount_amount = (line.product_qty * line.price_unit) - line.price_subtotal
            else:
                line.discount_amount = 0.0