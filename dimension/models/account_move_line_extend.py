from odoo import fields, models, api


from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    dimension = fields.Char(string="Dimension", readonly=True)

    # This method is triggered when the product_id changes.
    # It searches for a related stock.move record based on the sale order (invoice_origin)
    # and product, then sets the 'dimension' field in the account.move.line to match
    # the stock.move's dimension. If no such stock.move is found, it clears the dimension field.
    @api.onchange('product_id')
    def _onchange_product_id_dimension(self):
        for line in self:
            if not line.move_id or not line.product_id:
                continue

            sale_order = line.move_id.invoice_origin
            if not sale_order:
                continue

            stock_move = self.env['stock.move'].search([
                ('product_id', '=', line.product_id.id),
                ('origin', '=', sale_order),
                ('state', 'not in', ['cancel']),
            ], limit=1, order='id desc')

            if stock_move:
                line.dimension = stock_move.dimension
            else:
                line.dimension = False
