# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class talus_report_mods(models.Model):
#     _name = 'talus_report_mods.talus_report_mods'
#     _description = 'talus_report_mods.talus_report_mods'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
