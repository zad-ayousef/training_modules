from odoo import models, fields, api, exceptions
import re

from odoo.exceptions import ValidationError


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    phone = fields.Char(required=True)
    mobile = fields.Char(required=True)

    @api.constrains('phone', 'mobile')
    def _check_phone_and_mobile_digits(self):

        pattern = re.compile(r'^\d+$')
        for rec in self:
            if rec.phone and not pattern.match(rec.phone):
                raise ValidationError('Phone must contain only numbers.')
            if rec.mobile and not pattern.match(rec.mobile):
                raise ValidationError('mobile must contain only numbers.')
