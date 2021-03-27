odoo.define('talus_help.iorad_iframe_invadmin', function (require) {
'use strict';


var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var framework = require('web.framework');
var rpc = require('web.rpc');

// Inventory(Admin)
var iorad_iframe_invadmin = AbstractAction.extend({
   template: 'TalusIoradIframeViewInvAdmin',
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
                method: 'get_urlinvadmin',
                args: ['key',['args']],
            }).then(function (result) {
            if(result){
            //  setting the src of iframe to the returned value
            $('#iframeinventoryadmin').attr('src',result);
            }})},
});

// Inventory 
core.action_registry.add("iorad_iframe_invadmin", iorad_iframe_invadmin);

return iorad_iframe_invadmin;


});