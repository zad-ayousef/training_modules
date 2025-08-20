from odoo import models, fields


class ResConfigSettingsExtend(models.TransientModel):
    _inherit = 'res.config.settings'

    url = fields.Char(config_parameter='odoo_integration18.url')
    db_name = fields.Char(config_parameter='odoo_integration18.db_name')
    user_name = fields.Char(config_parameter='odoo_integration18.user_name')
    password = fields.Char(config_parameter='odoo_integration18.password')