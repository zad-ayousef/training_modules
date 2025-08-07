from odoo import models, fields, api, exceptions


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dimension = fields.Char("Dimension")
    
    is_editable = fields.Boolean(
        compute='_compute_is_editable',
        default=False,
        string='Is Editable'
    )

    # Computes whether the current user is allowed to edit the 'dimension' field
    # on this sale order line. Editing is only allowed for the salesperson
    # assigned to the order.
    def _compute_is_editable(self):
        for line in self:
            line.is_editable = line.order_id.user_id == self.env.user
    
    # When the product_id is changed, this function automatically sets
    # the dimension field based on the related product's dimension.
    @api.onchange('product_id')
    def _onchange_product_id_dimension(self):
        if self.product_id:
            self.dimension = self.product_id.dimension

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
