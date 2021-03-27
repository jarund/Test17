# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def default_get(self, fields_list):
        default_vals = super(StockMove, self).default_get(fields_list)
        default_vals['scrap_id'] = self.env.ref('stock_extend.product_category_scrap').id
        return default_vals

    # Used only for filter
    scrap_id = fields.Many2one('product.category')
