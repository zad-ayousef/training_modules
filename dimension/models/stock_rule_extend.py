from odoo import models


class StockRuleInherit(models.Model):
    _inherit = 'stock.rule'

    # Extends the list of fields to copy from the sale order line to the stock move by
    # adding 'dimension' to the list of custom move fields.
    def _get_custom_move_fields(self):
        fields = super()._get_custom_move_fields()
        fields += ['dimension']
        return fields
