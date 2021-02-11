odoo.define('web_environment_ribbon.ribbon', function(require) {
"use strict";

    require('web.dom_ready');
    var rpc = require('web.rpc');
    var core = require('web.core');

    // Code from: http://jsfiddle.net/WK_of_Angmar/xgA5C/
    function validStrColour(strToTest) {
        if (strToTest === "") {
            return false;
        }
        if (strToTest === "inherit") {
            return true;
        }
        if (strToTest === "transparent") {
            return true;
        }
        var image = document.createElement("img");
        image.style.color = "rgb(0, 0, 0)";
        image.style.color = strToTest;
        if (image.style.color !== "rgb(0, 0, 0)") {
            return true;
        }
        image.style.color = "rgb(255, 255, 255)";
        image.style.color = strToTest;
        return image.style.color !== "rgb(255, 255, 255)";
    }

    core.bus.on('web_client_ready', null, function () {
        var ribbon = $('<div class="test-ribbon hidden"/>');
        $('body').append(ribbon);
        ribbon.hide();
        // Get ribbon data from backend
        rpc.query({
            model: 'web.environment.ribbon.backend',
            method: 'get_environment_ribbon',
        }).then(
            function (ribbon_data) {
                // Ribbon name
                if (ribbon_data.name && ribbon_data.name !== 'False') {
                    ribbon.html(ribbon_data.name);
                    ribbon.show();
                }
                // Ribbon color
                if (ribbon_data.color && validStrColour(ribbon_data.color)) {
                    ribbon.css('color', ribbon_data.color);
                }
                // Ribbon background color
                if (ribbon_data.background_color && validStrColour(ribbon_data.background_color)) {
                    ribbon.css('background-color', ribbon_data.background_color);
                }
            }
        );
    });
});
