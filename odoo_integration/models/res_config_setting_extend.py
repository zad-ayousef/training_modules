from odoo import models, fields


class ResConfigSettingsExtend(models.TransientModel):
    _inherit = 'res.config.settings'

    url = fields.Char(config_parameter='odoo_integration.url')
    db_name = fields.Char(config_parameter='odoo_integration.db_name')
    user_name = fields.Char(config_parameter='odoo_integration.user_name')
    password = fields.Char(config_parameter='odoo_integration.password')