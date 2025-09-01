from odoo import models, fields


class ResConfigSettingsExtend(models.TransientModel):
    _inherit = 'res.config.settings'

    allowed_discount = fields.Boolean(
        string='Allowed Discount',
        config_parameter='discount.allowed_discount',
        help='Enable automatic discount accounting entries'
    )
    allowed_discount_account_sales_id = fields.Many2one(
        'account.account',
        domain=[('account_type', 'in', ['income', 'income_other'])],
        config_parameter='discount.allowed_discount_account_sales_id',
    )
    allowed_discount_account_purchase_id = fields.Many2one(
        'account.account',
        domain=[('account_type', '=', 'expense')],
        string='Allowed Discount Account Purchase',
        config_parameter='discount.allowed_discount_account_purchase_id',
    )
