from odoo import models

# Settings
class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    # function returning the value from system parameter for settings
    def get_urlsettings(self, args):
        return self.env['ir.config_parameter'].search([('key','=','help_settings.url')],limit=1).value

