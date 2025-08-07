from odoo import models, fields


class ProductTemplateExtend(models.Model):
    _inherit = 'product.template'

    dimension = fields.Char(string='Product Dimension')
