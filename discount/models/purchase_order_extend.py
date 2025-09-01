from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    total_discount = fields.Monetary(
        string='Total Discount',
        compute='_compute_total_discount',
        store=True,
        currency_field='currency_id',
    )

    @api.depends('order_line.price_subtotal', 'order_line.price_unit', 'order_line.product_qty')
    def _compute_total_discount(self):
        for order in self:
            total_before_discount = sum(line.product_qty * line.price_unit for line in order.order_line)
            order.total_discount = total_before_discount - order.amount_untaxed


