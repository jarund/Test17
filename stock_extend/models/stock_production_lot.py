# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.model
    def default_get(self, fields_list):
        default_vals = super(StockProductionLot, self).default_get(fields_list)
        default_vals['container_id'] = self.env.ref('stock_extend.product_category_container').id
        return default_vals

    container_id = fields.Many2one('product.category', readonly=True)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """ search full name and barcode """
        args = args or []
        if self._context.get('lot_search'):
            product_id = self._context.get('default_product_id')
            if name:
                args.append(('name', 'ilike', name))
            if self._context.get('picking_code') == 'incoming':
                args.append(('product_id', '=', product_id))
            if self._context.get('picking_code') == 'outgoing':
                args.append(('cmc_container', '!=', False))
            lot_ids = self.search(args, limit=limit)
            if self._context.get('picking_code') == 'outgoing':
                lot_ids = lot_ids.filtered(lambda l: l.product_qty > 0)
            return lot_ids.name_get()
        return super(StockProductionLot, self).name_search(name, args, operator, limit)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0,limit=None, order=None):
        if self._context.get('lot_search'):
            product_id = self._context.get('default_product_id')
            if self._context.get('picking_code') == 'incoming':
                domain.append(('product_id', '=', product_id))
            if self._context.get('picking_code') == 'outgoing':
                domain.append(('cmc_container', '!=', False))
        return super(StockProductionLot, self).search_read(domain, fields, offset, limit, order)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self._context.get('lot_search'):
            res = super(StockProductionLot, self).search(args, offset=offset, limit=limit, order=order, count=count)
            if self._context.get('picking_code') == 'outgoing':
                res = res.filtered(lambda r: r.product_qty > 0)
            return res
        return super(StockProductionLot, self).search(args, offset=offset, limit=limit, order=order, count=count)

    @api.model
    def create(self, vals):
        if vals.get('name'):
            container_id = self.env['product.template'].search([
                ('name', '=', vals.get('name')),
                ('categ_id', '=', self.env.ref('stock_extend.product_category_container').id)
            ], limit=1)
            if container_id:
                vals.update({
                    'cmc_container': container_id.id
                })
        res = super(StockProductionLot, self).create(vals)
        return res

    def _check_create(self):
        picking_type_id = self.env.context.get('default_picking_type_id', False)
        if picking_type_id:
            picking_type_id = self.env['stock.picking.type'].browse(picking_type_id)
            if picking_type_id and not picking_type_id.use_create_lots:
                raise UserError(_('You are not allowed to create a lot or serial number with this operation type. To change this, go on the operation type and tick the box "Create New Lots/Serial Numbers".'))
