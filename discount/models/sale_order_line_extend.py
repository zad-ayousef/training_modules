from odoo import models, fields, api


class SaleOrderLineExtend(models.Model):
    _inherit = 'sale.order.line'

    discount_amount = fields.Monetary(
        compute='_compute_discount_amount',
        store=True,
        currency_field='currency_id',
    )

    @api.depends('product_uom_qty', 'price_unit', 'price_subtotal', 'discount')
    def _compute_discount_amount(self):
        for line in self:
            if line.discount > 0 and line.product_uom_qty > 0 and line.price_unit > 0:
                line.discount_amount = (line.product_uom_qty * line.price_unit) - line.price_subtotal
            else:
                line.discount_amount = 0.0