odoo.define('sgb_get_weight.serial_port', function (require) {
"use strict";

var BasicController = require('web.BasicController');
var core = require('web.core');
var Dialog = require('web.Dialog');
var dialogs = require('web.view_dialogs');
var FormControllers = require('web.FormController');

var _t = core._t;
var qweb = core.qweb;
var rpc = require('web.rpc');
var Dialog = require('web.Dialog');
var QWeb = core.qweb;

FormControllers.include({
    _onButtonClicked: function (ev) {
        // stop the event's propagation as a form controller might have other
        // form controllers in its descendants (e.g. in a FormViewDialog)
        ev.stopPropagation();
        var self = this;
        this._super.apply(this, arguments);
        var attrs = ev.data.attrs;
        var ids = ev.data.record.data.id;
        var ids = ev.data.record.data.id;
        if((attrs.name == "get_weight")  || (attrs.name == "action_port_check" )){
            rpc.query({
                model: 'sgb.port',
                method: 'action_ports',
                args: ["s"],
            }, {
                shadow: true,
            }).then(function (url) {
                if (url){
                    var urls = url['ip_address']+":"+url['port_number']+url['api_url']+"?serial_port="+url['serial_port']+"&baudrate="+url['baudrate']+"&bytesize="+url['bytesize']+"&timeout="+url['timeout']+"&stopbits="+url['stopbits']
                    console.log("Urls",urls)
                     $.ajax({
                        type: 'POST',
                        data: {},
                        url: urls,
                        error: function (jqXHR, textStatus, errorThrown) {
                            alert("Not able to read the scale weight, please contact your Administrator.")
                        },
                        success: function (data) {
                            if (data){

                            }
                            self._rpc({
                                model: 'sgb.port',
                                method: 'action_weight_write',
                                args:[data,ids],
                            }).then(function (url) {
                                self.camera_popup(ids);
                            });
                        }
                    });
                }
            });
        }
        if(attrs.name == "open_webcam"){
            self.camera_popup(ids);
        }
    },
    camera_popup: function(ids){
        var self = this;
         Webcam.set({
                width: 320,
                height: 240,
                dest_width: 320,
                dest_height: 240,
                image_format: 'jpeg',
                jpeg_quality: 90,
                force_flash: false,
                fps: 45,
                swfURL: '/web_image_webcam/static/src/js/webcam.swf',
                //force_flash: true,
            });
            var WebCamDialog = $(QWeb.render("WebCamDialog")),
            img_data;
//

             var dialog = new Dialog(self, {
                    size: 'large',
                    dialogClass: 'o_act_window',
                    title: _t("WebCam Booth"),
                    $content: WebCamDialog,
                    buttons: [
                        {
                            text: _t("Save & Close"), classes: 'btn-primary save_close_btn', close: true,
                            click: function () {
                                if(img_data){
                                     var img_data_base64 = img_data.split(',')[1];
                                    var approx_img_size = 3 * (img_data_base64.length / 4)  // like... "3[n/4]"
                                    self.upload_image(img_data_base64,ids);
                                }else{
                                    alert("Take Photo")
                                }
                            }
                        },
                        {
                            text: _t("Close"), close: true
                        }
                    ]
                }).open();
                var w = Webcam.attach(WebCamDialog.find('#live_webcam')[0]);
                Webcam.on( 'load', function() {
                      Webcam.snap( function(data) {
                                img_data = data;
                                WebCamDialog.find("#webcam_result").html('<img src="'+img_data+'"/>');
                            });
                });

                $('.save_close_btn').attr('disabled', 'disabled');

                // Placeholder Image in the div "webcam_result"
                WebCamDialog.find("#webcam_result").html('<img src="/web_image_webcam/static/src/img/webcam_placeholder.png"/>');

    },
    upload_image: function(img_data_base64,ids){
        var self = this;
        self._rpc({
                    model: 'sgb.port',
                    method: 'action_image_write',
                    args:[img_data_base64,ids],
                }).then(function (url) {
                     console.log("without reload");
        });
    },

});
});
