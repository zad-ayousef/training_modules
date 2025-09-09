from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    add_limit = fields.Boolean(string="Add Limit")
    the_limit = fields.Integer(string="The Limit")

    @api.model
    def check_limit(self, product_id):
        try:
            product = self.browse(product_id)
            if not product.exists():
                return {"has_limit": False, "limit": 0, "name": product.name}

            if product.add_limit and product.the_limit > 0:
                return {"has_limit": True, "limit": product.the_limit, "name": product.name}

            return {"has_limit": False, "limit": 0}
        except Exception as e:
            _logger.error("Error in check_limit: %s", e)
            return {"has_limit": False, "limit": 0, "name": product.name}
