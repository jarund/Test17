# -*- coding: utf-8 -*-
from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.depends('move_line_nosuggest_ids', 'move_line_nosuggest_ids.lot_id')
    def _compute_warn(self):
        for rec in self:
            lot_list = []
            for move_line in rec.move_line_nosuggest_ids.filtered(lambda r: r.lot_id and not r.lot_id.cmc_container):
                lot_list.append(move_line.lot_id)
            lot_name = ''
            for l_id in lot_list:
                lot_name += l_id.name + '  '
            rec.warn = "No Container set for %s" % lot_name if lot_list else ''

    barcode = fields.Char("Barcode Scanned", help="Value of the last barcode scanned.")
    warn = fields.Char(" ", compute="_compute_warn", help="Show warning message for Lot not set Container")

    @api.onchange('barcode')
    def _on_barcode_scanned(self):
        ProductTemplate = self.env['product.template']
        if self.barcode:
            # if self.picking_type_id.code == 'incoming':
            #     container_id = ProductTemplate.search([
            #         ('categ_id', '=', self.env.ref('stock_extend.product_category_container').id),
            #         ('barcode', '=', self.barcode),
            #     ])
            #     if not container_id:
            #         raise ValidationError(_("Container is not available"))
            #     lot_id = self.env['stock.production.lot'].search([
            #         ('cmc_container', '=', container_id.id),
            #     ], limit=1)
            #     if not lot_id:
            #         raise ValidationError(_("Not lot found for container."))
            #     des_location_id = self.env['stock.location'].search([
            #         ('name', '=', 'Vendors')
            #     ], limit=1)
            #     vals = {
            #         'product_id': lot_id.product_id.id,
            #         'lot_id': lot_id.id,
            #         'product_uom_id': lot_id.product_id.uom_id.id,
            #         'location_dest_id': self.location_dest_id.id,
            #         'location_id': des_location_id.id,
            #         'company_id': self.company_id.id,
            #         'qty_done': lot_id.product_qty if lot_id.product_qty > 1 else 1,
            #     }
            #     new_line = self.move_line_nosuggest_ids.new(vals)
            #     new_line._onchange_product_id()
            #     self.move_line_nosuggest_ids += new_line
            #     self.move_line_ids_without_package = False
            if self.picking_type_id.code == 'outgoing':
                container_id = ProductTemplate.search([
                    ('categ_id', '=', self.env.ref('stock_extend.product_category_container').id),
                    ('barcode', '=', self.barcode),
                ])
                if not container_id:
                    raise ValidationError(_("Container is not available"))
                lot_ids = self.env['stock.production.lot'].search([
                    ('cmc_container', '=', container_id.id),
                ])
                if not lot_ids:
                    raise ValidationError(_("Not lot found for container."))
                else:
                    lot_ids = lot_ids.filtered(lambda l: l.product_qty > 0)
                des_location_id = self.env['stock.location'].search([
                    ('name', '=', 'Customers')
                ], limit=1)
                for lot_id in lot_ids:
                    new_line = self.move_line_ids_without_package.new({
                        'product_id': lot_id.product_id.id,
                        'lot_id': lot_id.id,
                        'product_uom_id': lot_id.product_id.uom_id.id,
                        'location_id': self.location_id.id,
                        'location_dest_id': des_location_id.id,
                        'company_id': self.company_id.id,
                        'qty_done': 0,
                    })
                    new_line._onchange_product_id()
                    self.move_line_ids_without_package += new_line
                    self.move_line_nosuggest_ids = False

    def _action_done(self):
        StockScrap = self.env['stock.scrap']
        StockPicking = self.env['stock.picking']
        virtual_location_id = self.env['stock.location'].search([
            ('name', '=', 'Inventory adjustment')
        ], limit=1)
        for move in self.filtered(lambda m: m.picking_type_id.code == 'outgoing'):
            for move_line in move.move_line_ids:
                # Create Scrap if done quantity is less than lot quantity
                if move_line.product_id.type in ('product', 'consu') and \
                        move_line.lot_id and \
                        move_line.lot_id.product_qty < move_line.qty_done:
                    picking_type_id = self.env['stock.picking.type'].search([
                        ('code', '=', 'internal')
                    ], limit=1)
                    if not picking_type_id:
                        raise ValidationError(_("Not Internal reference Found"))
                    diff_qty = move_line.qty_done - move_line.lot_id.product_qty
                    vals = {
                        'picking_type_id': picking_type_id.id,
                        'location_id': virtual_location_id.id,
                        'location_dest_id': move_line.location_id.id,
                        'move_line_nosuggest_ids': [(0, 0, {
                            'product_id': move_line.product_id.id,
                            'location_id': virtual_location_id.id,
                            'location_dest_id': move.location_id.id,
                            'lot_id': move_line.lot_id.id,
                            'qty_done': diff_qty,
                            'product_uom_id': move_line.product_uom_id.id
                        })]
                    }
                    picking_type_id = StockPicking.with_context(no_scrap=True).create(vals)
                    for l in picking_type_id.move_line_nosuggest_ids:
                        l._onchange_product_id()
                    picking_type_id.button_validate()
                    move_line.sudo().write({
                        'receipt_picking_id': picking_type_id.id,
                        'adjust_quantity': -abs(diff_qty)
                    })
        res = super(Picking, self)._action_done()
        for move in self.filtered(lambda m: m.picking_type_id.code == 'outgoing'):
            for move_line in move.move_line_ids:
                # Create Scrap if done quantity is less than lot quantity
                if move_line.product_id.type in (
                        'product', 'consu') and move_line.lot_id and move_line.lot_id.product_qty:
                    if move_line.lot_id.product_qty > 0:
                        move_line.sudo().write({
                            'adjust_quantity': move_line.lot_id.product_qty
                        })
                        stock_scrap_id = StockScrap.create({
                            'picking_id': move.id,
                            'product_id': move_line.product_id.id,
                            'scrap_qty': move_line.lot_id.product_qty,
                            'product_uom_id': move_line.product_uom_id.id,
                            'location_id': move_line.location_id.id,
                            'lot_id': move_line.lot_id.id
                        })
                        stock_scrap_id.action_validate()
        return res

    @api.model
    def create(self, vals):
        if not vals.get('picking_type_id'):
            vals.update({
                'picking_type_id': self._context.get('default_picking_type_id')
            })
        return super(Picking, self).create(vals)

    def button_validate(self):
        if self.picking_type_id.code == 'incoming' and \
                not self._context.get('button_validate') and \
                any(self.move_line_ids_without_package.filtered(lambda m: m.lot_id and not m.lot_id.cmc_container)):
            msg = ""
            for line in self.move_line_ids_without_package.filtered(lambda l: l.lot_id and not l.lot_id.cmc_container):
                msg += "%s, " % line.lot_id.name
            msg += "  lots don't have container set"
            wizard_id = self.env['stock.picking.confirm.wizard'].create({
                'picking_id': self.id,
                'msg': msg
            })
            return {
                'name': _('Confirmation'),
                'view_mode': 'form',
                'res_model': 'stock.picking.confirm.wizard',
                'res_id': wizard_id.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
                'context': {}
            }
        return super(Picking, self).button_validate()
