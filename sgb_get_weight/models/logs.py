
from odoo import models, fields, api, _

class Sgb_Logging(models.Model):
    _name = 'sgb.logging'
    _description = 'Log'

    create_date = fields.Datetime(string='Created on', readonly=True)
    name = fields.Char(required=True)
    message = fields.Text(required=True)
