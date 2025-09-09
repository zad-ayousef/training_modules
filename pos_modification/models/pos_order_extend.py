from odoo import models, fields, api


class PosOrderExtend(models.Model):
    _inherit = 'pos.order'

    attachment = fields.Binary(string="Attachment", readonly=True)
    attachment_filename = fields.Char(string="Attachment Filename", readonly=True)


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def save_closing_attachment(self, attachment_data=None, filename=None):
        if attachment_data and filename:
            current_session = self.search([
                ('state', '=', 'opened'),
                ('user_id', '=', self.env.user.id)
            ], limit=1)

            if current_session:
                try:
                    orders = current_session.order_ids
                    for order in orders:
                        order.write({
                            'attachment': attachment_data,
                            'attachment_filename': filename
                        })

                    return {
                        'success': True,
                        'message': f'Attachment saved to {len(orders)} orders'
                    }

                except Exception as e:
                    import logging
                    _logger = logging.getLogger(__name__)
                    _logger.error(f"Attachment saving error: {str(e)}")
                    return {'success': False, 'message': f'Error: {str(e)}'}
            else:
                return {'success': False, 'message': 'No open session found'}

        return {'success': False, 'message': 'No attachment data provided'}
