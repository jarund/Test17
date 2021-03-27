# -*- coding: utf-8 -*-
# from odoo import http


# class TalusReportMods(http.Controller):
#     @http.route('/talus_report_mods/talus_report_mods/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/talus_report_mods/talus_report_mods/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('talus_report_mods.listing', {
#             'root': '/talus_report_mods/talus_report_mods',
#             'objects': http.request.env['talus_report_mods.talus_report_mods'].search([]),
#         })

#     @http.route('/talus_report_mods/talus_report_mods/objects/<model("talus_report_mods.talus_report_mods"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('talus_report_mods.object', {
#             'object': obj
#         })
