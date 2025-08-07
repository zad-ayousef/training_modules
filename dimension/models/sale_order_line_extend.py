from odoo import models, fields, api, exceptions


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dimension = fields.Char("Dimension")

    # When the product_id is changed, this function automatically sets
    # the dimension field based on the related product's dimension.
    @api.onchange('product_id')
    def _onchange_product_id_dimension(self):
        if self.product_id:
            self.dimension = self.product_id.dimension

    # Overrides the create method to restrict setting the dimension field.
    # Only the salesperson assigned to the order can set the dimension when creating a sale order line.
    @api.model
    def create(self, vals):
        if 'dimension' in vals and vals.get('order_id'):
            order = self.env['sale.order'].browse(vals['order_id'])
            if order.exists() and order.user_id != self.env.user:
                raise exceptions.UserError("Only the salesperson assigned to this order can set dimension.")
        return super(SaleOrderLine, self).create(vals)

    # Overrides the write method to restrict editing the dimension field.
    # Only the salesperson assigned to the order can edit the dimension.
    def write(self, vals):
        if 'dimension' in vals:
            for line in self:
                if line.order_id.user_id != self.env.user:
                    raise exceptions.UserError("Only the salesperson assigned to this order can edit dimension.")
        return super(SaleOrderLine, self).write(vals)

    # Prepares custom procurement values by adding the dimension field when generating procurement for stock moves.
    def _prepare_procurement_values(self, group_id=False):
        res = super()._prepare_procurement_values(group_id)
        res['dimension'] = self.dimension
        return res

    # Prepares the invoice line values and sets the dimension key based on a related non-cancelled stock move if available.
    def _prepare_invoice_line(self, **optional_values):
        invoice_line_vals = super()._prepare_invoice_line(**optional_values)

        stock_move = self.move_ids.filtered(lambda m: m.state != 'cancel')[:1]

        if stock_move:
            invoice_line_vals['dimension'] = stock_move.dimension

        return invoice_line_vals
