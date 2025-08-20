from odoo import models, fields, api
from ..utils.remote_odoo import RemoteOdoo



class ProjectTask(models.Model):
    _inherit = 'project.task'

    related_task_id = fields.Integer(string="Related Task ID")

    def _get_remote_odoo(self):
        config = self.env['ir.config_parameter'].sudo()
        url = config.get_param('odoo_integration18.url')
        db_name = config.get_param('odoo_integration18.db_name')
        user_name = config.get_param('odoo_integration18.user_name')
        password = config.get_param('odoo_integration18.password')

        if not all([url, db_name, user_name, password]) or not password.strip():
            return None

        try:
            return RemoteOdoo(url, db_name, user_name, password)
        except Exception as e:
            print(f"Failed to connect to remote: {e}")
            return None

    def _prepare_remote_vals(self, vals):

        remote_vals = {}


        remote_vals['name'] = vals.get('name', self.name)
        remote_vals['description'] = vals.get('description', self.description or False)


        if 'project_id' in vals:
            if vals['project_id']:
                project = self.env['project.project'].browse(vals['project_id'])
                if project.exists() and project.related_project_id:
                    remote_vals['project_id'] = project.related_project_id
                else:
                    print(f"No related project found for project ID {vals['project_id']}")
                    return None
            else:
                remote_vals['project_id'] = False
        elif self.project_id and self.project_id.related_project_id:
            remote_vals['project_id'] = self.project_id.related_project_id
        else:
            print("No project mapping available")
            return None


        if 'stage_id' in vals:
            if vals['stage_id']:
                stage = self.env['project.task.type'].browse(vals['stage_id'])
                if stage.exists() and stage.related_stage_id:
                    remote_vals['stage_id'] = stage.related_stage_id
                else:
                    print(f"No related stage found for stage ID {vals['stage_id']}")
            else:
                remote_vals['stage_id'] = False
        elif self.stage_id and self.stage_id.related_stage_id:
            remote_vals['stage_id'] = self.stage_id.related_stage_id


        if 'user_ids' in vals:

            # vals['user_ids'] comes as [(6, 0, [ids])] format
            if vals['user_ids'] and len(vals['user_ids']) > 0:
                command = vals['user_ids'][0]
                if command == 6:
                    user_ids = command[2]
                    remote_vals['user_ids'] = [(6, 0, user_ids)]
                else:
                    remote_vals['user_ids'] = vals['user_ids']
            else:
                remote_vals['user_ids'] = [(6, 0, [])]
        elif hasattr(self, 'user_ids') and self.user_ids:
            remote_vals['user_ids'] = [(6, 0, [u.id for u in self.user_ids])]

        remote_vals['related_task_id'] = self.id
        remote_vals['sync_in_progress'] = True

        return remote_vals

    @api.model
    def create(self, vals):
        if vals.get('sync_in_progress'):
            vals.pop('sync_in_progress')
            return super().create(vals)

        rec = super().create(vals)

        remote = rec._get_remote_odoo()
        if remote:
            try:
                remote_vals = rec._prepare_remote_vals(vals)
                if remote_vals:
                    remote_id = remote.create('project.task', remote_vals)
                    if remote_id:
                        rec.related_task_id = remote_id
                        print(f"Task synced: Local {rec.id} → Remote {remote_id}")
                    else:
                        print("Failed to get remote ID from create operation")
            except Exception as e:
                print(f"Failed to sync task creation: {e}")

        return rec

    def write(self, vals):

        if vals.get('sync_in_progress'):
            vals.pop('sync_in_progress')
            return super().write(vals)


        sync_fields = {'name', 'description', 'project_id', 'stage_id', 'user_ids'}
        if not any(field in vals for field in sync_fields):
            return super().write(vals)

        result = super().write(vals)


        if not self.env.context.get('task_sync_in_progress'):
            sync_context = dict(self.env.context, task_sync_in_progress=True)

            remote = self._get_remote_odoo()
            if remote:
                for rec in self:
                    if rec.related_task_id:
                        try:
                            remote_vals = rec.with_context(sync_context)._prepare_remote_vals(vals)
                            if remote_vals:
                                remote_vals.pop('related_task_id', None)

                                remote.write('project.task', [rec.related_task_id], remote_vals)
                                print(f"Task updated: Local {rec.id} → Remote {rec.related_task_id}")
                        except Exception as e:
                            print(f"Failed to sync task update: {e}")

        return result




