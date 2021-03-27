
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class Sgb_SerialPort(models.Model):
    _name = 'sgb.port'

    name = fields.Char(string='Name')
    ip_address = fields.Char("Ip address",required=True, help="Ip address with protocol",default="http://127.0.0.1")
    port_number = fields.Char("Ip address port number",required=True,default="5000")
    serial_port = fields.Char("Serial Port",required=True,default="COM1")
    api_url = fields.Char("Api Url",required=True,default="/serialPortdata")
    active = fields.Boolean("Active",required=True)
    baudrate = fields.Integer("Baudrate",required=True, default=9600)
    bytesize = fields.Integer("Bytesize",required=True, default=8)
    timeout = fields.Integer("Timeout",required=True, default=1)
    stopbits = fields.Integer("Stopbits",required=True, default=1)

    @api.model_create_multi
    def create(self, vals_list):
        obj = self.env['sgb.port'].sudo().search([])
        for i in obj:
            i.write({
                'active': False
            })
        return super(Sgb_SerialPort, self).create(vals_list)

    def action_port_check(self):
        print("action")

    def action_ports(self):
        """
            Fetching Ports
        """
        i = self.env['sgb.port'].sudo().search([],limit=1)
        dict = {
            "name": i.name,
            "ip_address": i.ip_address,
            "port_number": i.port_number,
            "serial_port": i.serial_port,
            "api_url": i.api_url,
            "baudrate": i.baudrate,
            "bytesize": i.bytesize,
            "timeout": i.timeout,
            "stopbits": i.stopbits,
        }
        return dict

    @api.model
    def action_weight_write(self,data,ids):
        _logger.info("++++++===")
        _logger.info(data)
        
        weight = ''.join(filter(lambda i: i.isdigit(), data))
        result = []
        _logger.info(weight)
        if data:
            
            uom = self.env['uom.uom'].sudo().search([('name','=','lb')],limit=1)
            if data and ids:
                obj = self.env['stock.move.line'].sudo().search([('id','=',ids)], limit=1)

                if uom:
                    sucess = obj.write({
                        'product_uom_id': uom.id,
                    })
                sucess = obj.write({
                    'qty_done': float(weight),
                })
                return True
        else:
            raise ValidationError(_('Not able to read the scale weight, please contact your Administrator.'))
    @api.model
    def action_image_write(self, img_data_base64, ids):
        obj = self.env['stock.move.line'].sudo().search([('id', '=', ids)], limit=1)
        sucess = obj.update({
            'webcam_image': img_data_base64,
        })
        return True
