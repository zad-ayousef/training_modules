from odoo import models, fields


class ResConfigSettingsExtend(models.TransientModel):
    _inherit = 'res.config.settings'

    url = fields.Char(config_parameter='odoo_integration17.url')
    db_name = fields.Char(config_parameter='odoo_integration17.db_name')
    user_name = fields.Char(config_parameter='odoo_integration17.user_name')
    password = fields.Char(config_parameter='odoo_integration17.password')