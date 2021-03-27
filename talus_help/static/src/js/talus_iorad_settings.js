odoo.define('talus_help.iorad_iframe_settings', function (require) {
'use strict';

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');
var framework = require('web.framework');
var rpc = require('web.rpc');

    // settings
    var iorad_iframe_settings = AbstractAction.extend({
    template: 'TalusIoradIframeViewSettings',
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
                    method: 'get_urlsettings',
                    args: ['key',['args']],
                }).then(function (result) {
                if(result){
                //  setting the src of iframe to the returned value
                $('#iframesettings').attr('src',result);
                }})},
    });

    // settings
    core.action_registry.add("iorad_iframe_settings", iorad_iframe_settings);

    return iorad_iframe_settings;
});