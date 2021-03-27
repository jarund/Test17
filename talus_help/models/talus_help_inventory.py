from odoo import models

# Inventory
class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    # function returning the value from system parameter for inventory
    def get_urlinv(self, args):
        return self.env['ir.config_parameter'].search([('key','=','help_inventory.url')],limit=1).value

