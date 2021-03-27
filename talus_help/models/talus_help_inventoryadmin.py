from odoo import models

# Inventory(Admin)
class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    # function returning the value from system parameter for inventory
    def get_urlinvadmin(self, args):
        return self.env['ir.config_parameter'].search([('key','=','help_inventoryadmin.url')],limit=1).value

