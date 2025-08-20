from odoo import models, fields, api
from ..utils.remote_odoo import RemoteOdoo


class ProjectProject(models.Model):
    _inherit = 'project.project'

    related_project_id = fields.Integer(string="Related Project ID")

    def _get_remote_odoo(self):
        config = self.env['ir.config_parameter'].sudo()
        url = config.get_param('odoo_integration18.url')
        db_name = config.get_param('odoo_integration18.db_name')
        user_name = config.get_param('odoo_integration18.user_name')
        password = config.get_param('odoo_integration18.password')
        return RemoteOdoo(url, db_name, user_name, password)

    def _prepare_remote_vals(self, vals):
        remote_vals = {}
        remote_vals['name'] = vals.get('name', self.name)
        remote_vals['user_id'] = vals.get('user_id', self.user_id.id if self.user_id else False)
        remote_vals['description'] = vals.get('description', self.description)
        remote_vals['related_project_id'] = self.id

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
                remote_id = remote.create('project.project', remote_vals)
                if remote_id:
                    rec.related_project_id = remote_id
            except Exception as e:
                print(f"Failed to sync project creation: {e}")

        return rec

    def write(self, vals):

        if vals.get('sync_in_progress'):
            vals.pop('sync_in_progress')
            return super().write(vals)

        result = super().write(vals)
        remote = self._get_remote_odoo()
        for rec in self:
            if rec.related_project_id:
                try:
                    remote_vals = rec._prepare_remote_vals(vals)
                    remote.write('project.project', [rec.related_project_id], remote_vals)
                except Exception as e:
                    print(f"Failed to sync project update: {e}")
        return result


