# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPickingConfirmWizard(models.TransientModel):
    _name = 'stock.picking.confirm.wizard'
    _description = 'Immediate Transfer'

    picking_id = fields.Many2one('stock.picking', string="Picking")
    msg = fields.Char(string=" ", readonly='1')

    def action_confirm(self):
        self.picking_id.with_context(button_validate=True).button_validate()
