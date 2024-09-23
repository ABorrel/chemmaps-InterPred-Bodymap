var NTP = {
    printpage: '#printthispage',
    raAgencies: '#raAgencies',
    actualHostname: window.location.hostname.toLowerCase(),
    productionHostnames: ['ntp', 'www.ntp', 'ntp.niehs.nih.gov', 'www.ntp.niehs.nih.gov', 'tools.niehs.nih.gov', 'ntpsearch', 'ntpsearch.niehs.nih.gov', 'edit'],
    devHostNames: ['ntpdev', 'ntpdev.niehs.nih.gov', 'apps2dev.niehs.nih.gov', 'tools2dev.niehs.nih.gov', 'ntpsearch-dev', 'ntpsearch-dev.niehs.nih.gov', 'edit-dev'],
    testHostNames: ['ntptest', 'ntptest.niehs.nih.gov', 'apps2tst.niehs.nih.gov', 'tools2tst.niehs.nih.gov', 'ntpsearch-test', 'ntpsearch-test.niehs.nih.gov', 'edit-tst'],
    environment: 'Prod',
    PublicSiteHostName: 'https://ntp.niehs.nih.gov',
    isProduction: false
}

// check to see if we're on production
for (var i = 0; i < NTP.devHostNames.length; i++) {
    if (NTP.actualHostname === NTP.devHostNames[i]) {
        NTP.environment = 'Dev'
        NTP.PublicSiteHostName = 'https://ntpdev.niehs.nih.gov'
        break;
    }
}
for (var i = 0; i < NTP.testHostNames.length; i++) {
    if (NTP.actualHostname === NTP.testHostNames[i]) {
        NTP.environment = 'Test'
        NTP.PublicSiteHostName = 'https://ntptest.niehs.nih.gov'
        break;
    }
}
for (var i = 0; i < NTP.productionHostnames.length; i++) {
    if (NTP.actualHostname === NTP.productionHostnames[i]) {
        NTP.environment = 'Prod'
        NTP.PublicSiteHostName = 'https://ntp.niehs.nih.gov'
        NTP.isProduction = true
        break;
    }
}

// prevent cross-frame scripting by forcing the document to be the top - only for production instance
if (top != self) top.location = self.location;

$(function () {
    // register print this page event.
    $(NTP.printpage).attr('href', '#').click(function () { window.print(); });

    //register regulatory actions event.
    $(NTP.raAgencies).change(function () { location.href = "#" + $(this).val(); });
});

/*  this removes placeholder text before printing - Added by Mark Colebank 5/8/2015 
called in body tag on forms <body onbeforeprint="removePlaceholder()"> */
function removePlaceholder() {
    $("input").removeAttr("placeholder");
    $("textarea").removeAttr("placeholder");
}

/* Configure addthis sharing widget  */
var addthis_config = {
    // Prevent addthis buttons being first element to get focus on page when tabbing.
    ui_tabindex: 0,
    // Use a new tab/window for sharing (improved accessibility).
    ui_508_compliant: true
};

//adds IE support for includes() JS method - see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/includes
if (!String.prototype.includes) {
    String.prototype.includes = function() {
        'use strict';
        return String.prototype.indexOf.apply(this, arguments) !== -1;
    };
}

//define external link disclaimer title attribute; used within ntp.footer.js and ntp.external-links.js
var ntpExternalDisclaimer = 'This link is to a non-NTP website. Links do not constitute endorsement by NTP of the linked website. Visitors to the linked website will be subject to the website privacy policies. These practices may be different than those of this NTP website.';