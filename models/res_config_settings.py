from odoo import api, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    def _cl_clean_empty_binaries(self, vals):
        # Odoo 20 crashes ("'NoneType' object has no attribute 'filename'",
        # odoo/orm/fields_binary.py convert_to_cache) when an image field
        # arrives as {'content': False/'', 'filename': ...}.
        # Treat an empty upload as "no image" instead.
        for name, value in list(vals.items()):
            field = self._fields.get(name)
            if field and field.type == 'binary' and isinstance(value, dict) \
                    and 'content' in value and not value.get('content'):
                vals[name] = False
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._cl_clean_empty_binaries(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._cl_clean_empty_binaries(vals)
        return super().write(vals)
