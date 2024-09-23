// ===============================================================
// External Links (requires jQuery & ntp.common.js)
// ===============================================================

var ntpExtLinkClass = "external-link";
var ntpCurrentPage = window.location.href.toLowerCase();
var ntpLinkIdentify = 'a[href^="http://"], a[href^="https://"], a[href^="ftp://"], a[href^="//"]';
var ntpLinkInternalDefs = [
	'ntp.niehs.nih.gov',
	'ntptest.niehs.nih.gov',
	'ntpdev.niehs.nih.gov',
	'tools.niehs.nih.gov/webforms',
	'tools2tst.niehs.nih.gov/webforms',
	'tools2dev.niehs.nih.gov/webforms',
	'tools.niehs.nih.gov/mtreg',
	'tools2tst.niehs.nih.gov/mtreg',
	'tools2dev.niehs.nih.gov/mtreg',
	'ntpsearch.niehs.nih.gov',
	'ntpsearch-test.niehs.nih.gov',
	'ntpsearch-dev.niehs.nih.gov',
	'seek.niehs.nih.gov',
	'ehsthulp11',
	'ehsthult11',
	'edit/Rhythmyx',
	'edit-tst/Rhythmyx',
	'edit-dev/Rhythmyx',
	'edit:9992',
	'edit-tst:9992',
	'edit-dev:9992',
	'cebs.niehs.nih.gov',
	'tools.niehs.nih.gov/cebs3/',
	'tools2tst.niehs.nih.gov/cebs3/',
	'tools2dev.niehs.nih.gov/cebs3/',
	'doi.org'
];
var ntpLinkExternalDefs = [
	'/nnl',
	'/update',
	'/go/ntpupdate',
	'/annualreport',
	'/iccvamreport'
];
var NTPLinkInternal = 'a[href*=\'' + ntpLinkInternalDefs.join('\'], a[href*=\'') + '\']';
var ntpPDFLinks = 'a[href$=".pdf"]';

function ntpExternalLinks() {

	//add noopener noreferrer to all hard-coded target="_blank" to remediate window.opener vulnerability
	$('a[target="_blank"]').attr('rel', 'noopener noreferrer');

	//--- EXTERNAL SITES
	//add external link icon, target="_blank", rel="noopener noreferrer", and privacy disclaimer to links for domains that are not defined as internal
	$(ntpLinkIdentify).not(NTPLinkInternal).attr({
		'target': '_blank',
		'rel': 'noopener noreferrer',
		'title': ntpExternalDisclaimer
	}).addClass(ntpExtLinkClass);

	//--- INTERNAL SUBSITES
	//add or remove external link icon to internal subsites defined as external in ntpLinkExternalDefs
	$.each(ntpLinkExternalDefs, function() {

		if (ntpCurrentPage.includes(this)) {
			if (!this.includes('/nnl')) {
				//add external link icon and target="_blank" to internal links that are not within the current subsite (non-Atlas only)
				$(NTPLinkInternal).add('a[href^="/"]').not('a[href*="' + this + '"]').not(ntpPDFLinks).attr('target', '_blank').addClass(ntpExtLinkClass);
			}
		} else {
			//add external link icon and target="_blank" to internal subsite links
			$('a[href*="' + this + '"]').not(ntpPDFLinks).attr('target', '_blank').addClass(ntpExtLinkClass);
		}

	});

	//remove external link icons from header/footer logos and landing page images
	$('.header-logo img, #masthead img, .footer-logos img, .ntpLanding img').parent('a[target="_blank"]').removeClass(ntpExtLinkClass + ' external');

	//--- PDFS
	//open PDF files in new window by default 
	$(ntpPDFLinks).attr({
		'target': '_blank',
		'rel': 'noopener noreferrer'
	});

	//add external PDF link icon to external PDFs
	$(ntpPDFLinks).not($(NTPLinkInternal).add('a[href^="/"]')).addClass(ntpExtLinkClass + ' pdf');

}

function ntpModalExternalLinks() {
	$('.modal-content').each(function() {

		//add noopener noreferrer to all hard-coded target="_blank" to remediate window.opener vulnerability
		$(this).find('a[target="_blank"]').attr('rel', 'noopener noreferrer').addClass(ntpExtLinkClass);
		
		
		//add external link icon, target="_blank", rel="noopener noreferrer", and privacy disclaimer to all links to domains that are not defined as internal
		$(this).find(ntpLinkIdentify).not(NTPLinkInternal).attr({
			'target': '_blank',
			'rel': 'noopener noreferrer',
			'title': ntpExternalDisclaimer
		}).addClass(ntpExtLinkClass);
		
		//add or remove external link icon to internal subsites defined as external in ntpLinkExternalDefs
		$.each(ntpLinkExternalDefs, function() {

			if (ntpCurrentPage.includes(this)) {
				if (this !== '/nnl') {
					//add external link icon and target="_blank" to internal links that are not within the current subsite (non-Atlas only)
					$(this).find(NTPLinkInternal).add('a[href^="/"]').not('a[href*="' + this + '"]').not(ntpPDFLinks).attr('target', '_blank').addClass(ntpExtLinkClass);
				}
			} else {
				//add external link icon and target="_blank" to internal subsite links
				$(this).find('a[href*="' + this + '"]').not(ntpPDFLinks).attr('target', '_blank').addClass(ntpExtLinkClass);
			}

		});

		//open PDF files in new window by default
		$(this).find(ntpPDFLinks).attr({
			'target': '_blank',
			'rel': 'noopener noreferrer'
		});
		
		//add external PDF link icon to external PDFs
		$(this).find(ntpPDFLinks).not($(NTPLinkInternal).add('a[href^="/"]')).addClass(ntpExtLinkClass + ' pdf');
		
	});
}	
	
$(document).ready(function(){
	ntpExternalLinks();
});