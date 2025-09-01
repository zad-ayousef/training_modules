from odoo import models, fields, api


class SaleOrderExtend(models.Model):
    _inherit = 'sale.order'

    total_discount = fields.Monetary(
        compute='_compute_total_discount',
        store=True,
        currency_field='currency_id',
    )

    @api.depends('order_line.discount_amount')
    def _compute_total_discount(self):
        for order in self:
            order.total_discount = sum(line.discount_amount for line in order.order_line)
