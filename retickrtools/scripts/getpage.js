var page = require('webpage').create(),
    system = require('system'),
    url;

if (system.args.length == 1) {
    console.log('Usage: getpage.js <some URL>');
    phantom.exit();
}

url = system.args[1];
ua = system.args[2];

page.settings.userAgent = ua;

page.open(url, function (status) {
    if (status != 'success') {
        console.log('EPIC FAIL');
    } else {
        var txt = page.evaluate(function () {
            return document.documentElement.outerHTML;
        });
        console.log(txt);
    }
    phantom.exit();
});
