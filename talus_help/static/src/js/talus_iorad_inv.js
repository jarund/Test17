odoo.define('talus_help.iorad_iframe_inv', function (require) {
'use strict';


var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var framework = require('web.framework');
var rpc = require('web.rpc');

// Inventory 
var iorad_iframe_inv = AbstractAction.extend({
   template: 'TalusIoradIframeViewInv',
   init: function(parent, context) {
        this._super(parent, context);
    },
    start: function() {
        var self = this;
        return this._super().then(function() {
            self.render_values();
        });
    },
    // Calling rpc call to get the value from system parameter
    render_values: function() {
        var self = this;
        rpc.query({
                model: 'ir.config_parameter',
                method: 'get_urlinv',
                args: ['key',['args']],
            }).then(function (result) {
            if(result){
            //  setting the src of iframe to the returned value
            $('#iframeinventory').attr('src',result);
            }})},
});

// Inventory 
core.action_registry.add("iorad_iframe_inv", iorad_iframe_inv);

return iorad_iframe_inv;


});