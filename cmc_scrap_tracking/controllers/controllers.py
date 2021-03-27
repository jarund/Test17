# -*- coding: utf-8 -*-
# from odoo import http


# class CmcScrapTracking(http.Controller):
#     @http.route('/cmc_scrap_tracking/cmc_scrap_tracking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cmc_scrap_tracking/cmc_scrap_tracking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cmc_scrap_tracking.listing', {
#             'root': '/cmc_scrap_tracking/cmc_scrap_tracking',
#             'objects': http.request.env['cmc_scrap_tracking.cmc_scrap_tracking'].search([]),
#         })

#     @http.route('/cmc_scrap_tracking/cmc_scrap_tracking/objects/<model("cmc_scrap_tracking.cmc_scrap_tracking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cmc_scrap_tracking.object', {
#             'object': obj
#         })
