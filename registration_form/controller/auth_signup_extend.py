from odoo import http
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


class AuthSignupExtended(AuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        # catch custom fields
        mobile = kw.get('mobile')
        phone = kw.get('phone')
        #Call super
        response = super().web_auth_signup(*args, **kw)

        if kw.get('login'):
            user = request.env['res.users'].sudo().search(
                [('login', '=', kw.get('login'))], limit=1
            )
            if user and user.partner_id:
                user.partner_id.sudo().write({
                    'mobile': mobile,
                    'phone': phone
                })

        return response
