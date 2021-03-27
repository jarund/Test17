# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools


# Adding fields to product.teamplate
class cmc_product(models.Model):
    _inherit = 'product.template'
    # Model fields
    # 1/22/21 - Changed string from "Container" to "Container Type"
    cmc_container_type_ids = fields.Many2one('container_types', string="Container Type")


# Container Types on Product screen for Containers
class cmc_container_types(models.Model):
    _name = 'container_types'
    _description = 'Container Types'
    # Model fields
    name = fields.Char("Carrier Type")
    product_ids = fields.One2many('product.template', 'cmc_container_type_ids')


# Adding fields for Container tracking and weights on Lots
class cmc_lot_container(models.Model):
    _inherit = 'stock.production.lot'
    # Additional Model Fields
    cmc_container = fields.Many2one('product.template', string="Container")
    cmc_tare_weight = fields.Float(related='cmc_container.weight', string="Tare Weight")
    cmc_net_weight = fields.Float("Net Weight", compute='_compute_net')

    # Calculating Net Weight
    @api.depends('product_qty', 'cmc_container.weight', 'quant_ids', '__last_update')
    def _compute_net(self):
        for record in self:
            record.cmc_net_weight = record.product_qty - record.cmc_container.weight


# Adding fields on Inventory Report
class cmc_inventory_report(models.Model):
    _inherit = 'stock.quant'
    # Model fields - Adding related to pull into report
    cmc_lot_container = fields.Many2one(related='lot_id.cmc_container')
    cmc_lot_tare_weight = fields.Float(related='lot_id.cmc_tare_weight')
    cmc_lot_net_weight = fields.Float("Net Weight", compute='_compute_net', store=True)
    cmc_lot_gross_weight = fields.Float(related='lot_id.product_qty', string='Gross Weight')
    product_category = fields.Many2one(related='product_id.categ_id')

    @api.depends('inventory_quantity', 'lot_id.cmc_tare_weight')
    def _compute_net(self):
        for record in self:
            record.cmc_lot_net_weight = record.inventory_quantity - record.cmc_lot_tare_weight


# tools must be added to import in top of file
class cmc_container_report(models.Model):
    _name = 'cmc.container.report'
    _description = 'Used for CMC Container Report'
    _rec_name = 'product_id'
    _auto = False
    product_id = fields.Many2one(comodel_name='product.product', string='Scarp', readonly=True)
    categ_id = fields.Many2one(comodel_name='product.category', string='Product Category', readonly=True)
    location_id = fields.Many2one(comodel_name='stock.location', string='Location', readonly=True)
    lot_id = fields.Many2one(comodel_name='stock.production.lot', string='Lot#', readonly=True)
    quantity = fields.Float("Gross Weight", readonly=True)
    uom_id = fields.Many2one(comodel_name='uom.uom', string='UOM', readonly=True)
    cmc_container = fields.Many2one(comodel_name='product.template', string='Container', readonly=True)
    cmc_tare_weight = fields.Float("Tare Weight", readonly=True)
    cmc_net_weight = fields.Float("Net Weight", readonly=True)
    # @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'cmc_container_report')
        self._cr.execute(""" CREATE VIEW cmc_container_report AS (
            SELECT
                s.id as id,
                cast(s.product_id as integer) as product_id,
                cast(pts.categ_id as integer) as categ_id,
                s.location_id as location_id,
                s.lot_id as lot_id,
                SUM(s.quantity) as quantity,
                pt.uom_id as uom_id,
                l.cmc_container as cmc_container,
                SUM(pt.weight) as cmc_tare_weight,
                SUM(s.quantity - pt.weight) as cmc_net_weight
            FROM
                stock_quant s
            LEFT JOIN
                stock_production_lot l on (s.lot_id = l.id)
            LEFT JOIN
                product_template pt on (l.cmc_container = pt.id)
            LEFT JOIN
                product_template pts on (s.product_id = pts.id)
            LEFT JOIN
                stock_location loc on (s.location_id = loc.id)
            WHERE
                s.quantity > 0
                and loc.usage = 'internal'
            GROUP BY
                s.id,
                s.product_id,
                pts.categ_id,
                s.lot_id,
                s.location_id,
                pt.uom_id,
                l.cmc_container
        )""") 


# Adding fields on Operations
# Should show just for Shipments Out
class cmc_shipping(models.Model):
    _inherit = 'stock.picking'
    # Model fields
    cmc_load_date = fields.Date("Load Date")
    cmc_ship_date = fields.Date("Ship Date")
    cmc_truck_nbr = fields.Char("Truck Number")
    cmc_trailer_number = fields.Char("Trailer Number")
    cmc_seal_number = fields.Char("Seal Number")
    cmc_carrier_ids = fields.Many2one('cmc_carriers', string="Carrier")
    # type_of_operation = fields.Selection(related='picking_type_id.code')
    # cmc_shipment_customer_id = fields.Many2one('res.partner', string="Customer")


# Link to Contact(Customer)
""" class cmc_customer(models.Model):
    _inherit = 'res.partner'
    cmc_shipments = fields.One2many('stock.picking', 'cmc_shipment_customer_id', 'Shipments') """


# Carrier List
class cmc_carriers(models.Model):
    _name = 'cmc_carriers'
    _description = 'Carriers'
    # Model fields
    name = fields.Char("Carrier ID")
    description = fields.Char("Carrier Name")
    shipment_ids = fields.One2many('stock.picking', 'cmc_carrier_ids')
