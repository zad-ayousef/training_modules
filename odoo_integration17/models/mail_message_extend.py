from odoo import models, api


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, vals):

        if vals.get('sync_in_progress'):
            vals.pop('sync_in_progress')
            return super().create(vals)

        if vals.get('message_type') in ['notification', 'user_notification']:
            return super().create(vals)

        if self.env.context.get('chatter_sync_in_progress'):
            return super().create(vals)

        msg = super().create(vals)

        model = vals.get('model')
        res_id = vals.get('res_id')

        if model in ['project.project', 'project.task'] and res_id:
            try:
                record = self.env[model].browse(res_id)
                if not record.exists():
                    return msg

                if model == 'project.project':
                    related_id = getattr(record, 'related_project_id', None)
                else:
                    related_id = getattr(record, 'related_task_id', None)

                if related_id:
                    remote_odoo = record._get_remote_odoo()
                    if remote_odoo:

                        remote_vals = self._prepare_remote_message_vals(vals, related_id)

                        if remote_vals:

                            sync_context = dict(self.env.context, chatter_sync_in_progress=True)

                            remote_msg_id = remote_odoo.create('mail.message', remote_vals)
                            if remote_msg_id:
                                print(f"Message synced: Local {msg.id} → Remote {remote_msg_id}")
                            else:
                                print("Failed to create remote message")
            except Exception as e:
                print(f"Failed to sync message: {e}")

        return msg

    def _prepare_remote_message_vals(self, vals, related_res_id):

        try:
            remote_vals = {
                'subject': vals.get('subject', ''),
                'body': vals.get('body', ''),
                'message_type': vals.get('message_type', 'comment'),
                'subtype_id': vals.get('subtype_id', False),
                'model': vals.get('model'),
                'res_id': related_res_id,
                'author_id': vals.get('author_id', False),
                'email_from': vals.get('email_from', ''),
                'reply_to': vals.get('reply_to', ''),
                'record_name': vals.get('record_name', ''),
                'sync_in_progress': True
            }

            remote_vals = {k: v for k, v in remote_vals.items() if v is not False and v != ''}

            return remote_vals
        except Exception as e:
            print(f"Error preparing remote message values: {e}")
            return None
