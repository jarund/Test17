# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.model
    def default_get(self, fields_list):
        default_vals = super(StockMoveLine, self).default_get(fields_list)
        default_vals['scrap_id'] = self.env.ref('stock_extend.product_category_scrap').id
        return default_vals

    # Used only for filter
    scrap_id = fields.Many2one('product.category')
    product_id = fields.Many2one('product.product',
                                 'Product',
                                 ondelete="cascade",
                                 check_company=True,
                                 domain="[('type', '!=', 'service'), ('categ_id', '=', scrap_id), '|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    receipt_picking_id = fields.Many2one('stock.picking', string="Receipt Picking")
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        domain="[('company_id', '=', company_id)]",
        check_company=True)
    picking_code = fields.Selection(related='picking_id.picking_type_id.code', readonly=True, store=True)
    adjust_quantity = fields.Float(string="Adjusted Quantity")

    @api.onchange('lot_id')
    def _onchange_lot(self):
        if self.lot_id and not self.product_id:
            self.product_id = self.lot_id.product_id

    @api.model
    def create(self, vals):
        if vals.get('lot_id') and vals.get('product_id'):
            lot_obj = self.env['stock.production.lot'].browse(vals.get('lot_id'))
            product_obj = self.env['product.product'].browse(vals.get('product_id'))
            if lot_obj.product_id.id != vals.get('product_id'):
                raise ValidationError(_("Lot %s is not belongs to the Product (%s).")
                                      % (lot_obj.name, product_obj.name))
        return super(StockMoveLine, self).create(vals)
