"use strict";
var page = require('webpage').create(),
    system = require('system'),
    address, output, size;

address = system.args[1];
output = system.args[2];
var width = 900
var height = 400
page.viewportSize = { width: width, height: height };
page.clipRect = { top: 30, left: 10, width: width-30, height: height-35 };

page.open(address, function (status) {
    if (status !== 'success') {
        console.log('Unable to load the address!');
        phantom.exit(1);
    } else {
        window.setTimeout(function () {
            page.render(output);
            phantom.exit();
        }, 1000);
    }
});