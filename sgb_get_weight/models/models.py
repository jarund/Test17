# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import serial
from collections import namedtuple


def _toledo8217StatusParse(status):
    """ Parse a scale's status, returning a `(weight, weight_info)` pair. """
    weight, weight_info = None, None
    stat = status[status.index(b'?') + 1]
    if stat == 0:
        weight_info = 'ok'
    else:
        weight_info = []
        if stat & 1 :
            weight_info.append('moving')
        if stat & 1 << 1:
            weight_info.append('over_capacity')
        if stat & 1 << 2:
            weight_info.append('negative')
            weight = 0.0
        if stat & 1 << 3:
            weight_info.append('outside_zero_capture_range')
        if stat & 1 << 4:
            weight_info.append('center_of_zero')
        if stat & 1 << 5:
            weight_info.append('net_weight')
    return weight, weight_info

ScaleProtocol = namedtuple(
    'ScaleProtocol',
    "name baudrate bytesize stopbits parity timeout writeTimeout weightRegexp statusRegexp "
    "statusParse commandTerminator commandDelay weightDelay newWeightDelay disable "
    "weightCommand zeroCommand tareCommand clearCommand emptyAnswerValid autoResetWeight")
# https://www.python.org/downloads/release/python-392/


# 8217 Mettler-Toledo (Weight-only) Protocol, as described in the scale's Service Manual.
#    e.g. here: https://www.manualslib.com/manual/861274/Mettler-Toledo-Viva.html?page=51#manual
# Our recommended scale, the Mettler-Toledo "Ariva-S", supports this protocol on
# both the USB and RS232 ports, it can be configured in the setup menu as protocol option 3.
# We use the default serial protocol settings, the scale's settings can be configured in the
# scale's menu anyway.
Toledo8217Protocol = ScaleProtocol(
    name='Toledo 8217',
    baudrate=9600,
    bytesize=serial.SEVENBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_EVEN,
    timeout=1,
    writeTimeout=1,
    weightRegexp=b"\x02\\s*([0-9.]+)N?\\r",
    statusRegexp=b"\x02\\s*(\\?.)\\r",
    statusParse=_toledo8217StatusParse,
    commandDelay=0.2,
    weightDelay=0.5,
    newWeightDelay=0.2,
    commandTerminator=b'',
    weightCommand=b'W',
    zeroCommand=b'Z',
    tareCommand=b'T',
    clearCommand=b'C',
    emptyAnswerValid=False,
    autoResetWeight=False,
    disable=False
)

# The ADAM scales have their own RS232 protocol, usually documented in the scale's manual
#   e.g at https://www.adamequipment.com/media/docs/Print%20Publications/Manuals/PDF/AZEXTRA/AZEXTRA-UM.pdf
#          https://www.manualslib.com/manual/879782/Adam-Equipment-Cbd-4.html?page=32#manual
# Only the baudrate and label format seem to be configurable in the AZExtra series.
ADAMEquipmentProtocol = ScaleProtocol(
    name='Adam Equipment',
    baudrate=4800,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    timeout=0.2,
    writeTimeout=0.2,
    weightRegexp=b"\s*([0-9.]+)kg", # LABEL format 3 + KG in the scale settings, but Label 1/2 should work
    statusRegexp=None,
    statusParse=None,
    commandTerminator=b"\r\n",
    commandDelay=0.2,
    weightDelay=0.5,
    newWeightDelay=5,  # AZExtra beeps every time you ask for a weight that was previously returned!
                       # Adding an extra delay gives the operator a chance to remove the products
                       # before the scale starts beeping. Could not find a way to disable the beeps.
    weightCommand=b'P',
    zeroCommand=b'Z',
    tareCommand=b'T',
    clearCommand=None, # No clear command -> Tare again
    emptyAnswerValid=True, # AZExtra does not answer unless a new non-zero weight has been detected
    autoResetWeight=True,  # AZExtra will not return 0 after removing products
    disable=True
)


SCALE_PROTOCOLS = (
    Toledo8217Protocol,
    ADAMEquipmentProtocol, # must be listed last, as it supports no probing!
)



class Stock_Move_Inherite(models.Model):
    _inherit = 'stock.move'
    _description = 'stock_move_inherited'

    webcam_image = fields.Binary(string="Webcam Image")

    def _get_raw_response(self, connection):
        """Get Weight From Weight Scale Obj"""
        answer = []
        while True:
            char = connection.read(1)  # may return `bytes` or `str`
            if not char:
                break
            else:
                answer.append(bytes(char))
        return b''.join(answer)


    def get_weight(self):
        if self:
            import serial
            import io
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            print("default port", ports)
        #     serialPort = serial.Serial(port="COM2", baudrate=9600,
        #                                bytesize=8, timeout=1, stopbits=1)
        #     line = serialPort.readline()
        #     print("liness",line)
            # ser = serial.Serial()
            # ser.baudrate = 19200
            # ser.port = 'COM5'
            # ser.timeout=1
            # ser.open()
            # ser.is_open
            # ser.write(d.encode('utf-8'))
            # print("port open or not",ser.is_open)
            # while (1):
            #     print("data in waiting", serialPort.in_waiting)
            # # if (ser.in_waiting > 0):
            #     serialString = serialPort.readline()
            #     print(serialString)
            # for i in range(10):
            #     byte = ser.read(100000)
            #     print("port byte data stream",byte,len(byte))
            # print("is_open after", ser.readlines())

            # raise ValidationError(_(
            #     "Weighing Scale Is Not Loading... "))
        return

    def open_webcam(self):
        return

    def get_info_from_dev(self):
        """Ubuntu System"""
        import serial
        import time
        ser = serial.Serial('/dev/ttyUSB0',
                            baudrate=9600,
                            parity=serial.PARITY_EVEN,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.SEVENBITS,
                            timeout=1)

        while True:
            print(ser.read())
            return ser.read()

    class Stock_Move_Line_Inherite(models.Model):
        _inherit = 'stock.move.line'
        _description = 'stock_move_line_inherited'

        webcam_image = fields.Binary(string="Webcam Image")

        def _get_raw_response(self, connection):
            """Get Weight From Weight Scale Obj"""
            answer = []
            while True:
                char = connection.read(1)  # may return `bytes` or `str`
                if not char:
                    break
                else:
                    answer.append(bytes(char))
            return b''.join(answer)

        def get_weight(self):
            if self:
                import serial
                import io
                import serial.tools.list_ports
                ports = serial.tools.list_ports.comports()
                print("default port", ports)
            #     serialPort = serial.Serial(port="COM2", baudrate=9600,
            #                                bytesize=8, timeout=1, stopbits=1)
            #     line = serialPort.readline()
            #     print("liness",line)
            # ser = serial.Serial()
            # ser.baudrate = 19200
            # ser.port = 'COM5'
            # ser.timeout=1
            # ser.open()
            # ser.is_open
            # ser.write(d.encode('utf-8'))
            # print("port open or not",ser.is_open)
            # while (1):
            #     print("data in waiting", serialPort.in_waiting)
            # # if (ser.in_waiting > 0):
            #     serialString = serialPort.readline()
            #     print(serialString)
            # for i in range(10):
            #     byte = ser.read(100000)
            #     print("port byte data stream",byte,len(byte))
            # print("is_open after", ser.readlines())

            # raise ValidationError(_(
            #     "Weighing Scale Is Not Loading... "))
            return

        def open_webcam(self):
            return

        def get_info_from_dev(self):
            """Ubuntu System"""
            import serial
            import time
            ser = serial.Serial('/dev/ttyUSB0',
                                baudrate=9600,
                                parity=serial.PARITY_EVEN,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.SEVENBITS,
                                timeout=1)

            while True:
                print(ser.read())
                return ser.read()


    # def get_device(self):
    #     if self.device:
    #         return self.device
    #
    #     with hw_proxy.rs232_lock:
    #         try:
    #             if not os.path.exists(self.input_dir):
    #                 self.set_status('disconnected', 'No RS-232 device found')
    #                 return None
    #
    #             forbidden_devices = [os.readlink(self.forbidden_dir + d) for d in listdir(self.forbidden_dir) if
    #                                  'usb-Sylvac_Power_USB_A32DV5VM' in d]  # Skip special usb link with Sylvac
    #             devices = [device for device in listdir(self.input_dir) if
    #                        os.readlink(self.input_dir + device) not in forbidden_devices]
    #             for device in devices:
    #                 path = self.input_dir + device
    #                 driver = hw_proxy.rs232_devices.get(device)
    #                 if driver and driver != DRIVER_NAME:
    #                     # belongs to another driver
    #                     _logger.info('Ignoring %s, belongs to %s', device, driver)
    #                     continue
    #
    #                 for protocol in SCALE_PROTOCOLS:
    #                     _logger.info('Probing %s with protocol %s', path, protocol)
    #                     connection = serial.Serial(path,
    #                                                baudrate=protocol.baudrate,
    #                                                bytesize=protocol.bytesize,
    #                                                stopbits=protocol.stopbits,
    #                                                parity=protocol.parity,
    #                                                timeout=1,  # longer timeouts for probing
    #                                                writeTimeout=1)  # longer timeouts for probing
    #                     connection.write(protocol.weightCommand + protocol.commandTerminator)
    #                     # time.sleep(protocol.commandDelay)
    #                     answer = self._get_raw_response(connection)
    #                     weight, weight_info, status = self._parse_weight_answer(protocol, answer)
    #                     # if status:
    #                         # _logger.info('Probing %s: no valid answer to protocol %s', path, protocol.name)
    #                     # else:
    #                         # _logger.info('Probing %s: answer looks ok for protocol %s', path, protocol.name)
    #                         # self.path_to_scale = path
    #                         # self.protocol = protocol
    #                         # self.set_status(
    #                         #     'connected',
    #                         #     'Connected to %s with %s protocol' % (device, protocol.name)
    #                         # )
    #                         # connection.timeout = protocol.timeout
    #                         # connection.writeTimeout = protocol.writeTimeout
    #                         # hw_proxy.rs232_devices[path] = DRIVER_NAME
    #                         # return connection
    #
    #             self.set_status('disconnected', 'No supported RS-232 scale found')
    #         except Exception as e:
    #             # _logger.exception('Failed probing for scales')
    #             self.set_status('error', 'Failed probing for scales: %s' % e)
    #         return None