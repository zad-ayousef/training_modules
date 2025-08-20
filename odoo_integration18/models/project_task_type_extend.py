from odoo import models, fields, api
from ..utils.remote_odoo import RemoteOdoo


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    related_stage_id = fields.Integer(string="Related Stage ID")

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
        remote_vals['sequence'] = vals.get('sequence', self.sequence)
        remote_vals['fold'] = vals.get('fold', self.fold)

        related_project_ids = []
        if hasattr(self, 'project_ids'):
            for project in self.project_ids:
                if hasattr(project, 'related_project_id') and project.related_project_id:
                    related_project_ids.append(project.related_project_id)
            if related_project_ids:
                remote_vals['project_ids'] = [(6, 0, related_project_ids)]

        remote_vals['related_stage_id'] = self.id
        remote_vals['sync_in_progress'] = True

        return remote_vals

    @api.model
    def create(self, vals):
        if vals.get('sync_in_progress'):
            vals.pop('sync_in_progress')
            return super().create(vals)

        stage = super().create(vals)
        remote = stage._get_remote_odoo()

        if remote:
            try:
                remote_vals = stage._prepare_remote_vals(vals)
                remote_id = remote.create('project.task.type', remote_vals)

                if remote_id:
                    stage.related_stage_id = remote_id
                    print(f"Stage mapping created: Local ID {stage.id} ↔ Remote ID {remote_id}")

                    try:
                        remote.write('project.task.type', [remote_id], {'related_stage_id': stage.id})
                        print(f"Bidirectional mapping completed: {stage.id} ↔ {remote_id}")
                    except Exception as e:
                        print(f"Failed to update remote stage mapping: {e}")

            except Exception as e:
                print(f"Failed to sync stage creation: {e}")

        return stage

    def write(self, vals):
        if vals.get('sync_in_progress'):
            vals.pop('sync_in_progress')
            return super().write(vals)

        result = super().write(vals)
        remote = self._get_remote_odoo()

        if remote:
            for rec in self:
                if rec.related_stage_id:
                    try:
                        remote_vals = rec._prepare_remote_vals(vals)
                        remote_vals.pop('related_stage_id', None)
                        remote.write('project.task.type', [rec.related_stage_id], remote_vals)
                        print(f"Stage updated: Local {rec.id} → Remote {rec.related_stage_id}")
                    except Exception as e:
                        print(f"Failed to sync stage update: {e}")
        return result

