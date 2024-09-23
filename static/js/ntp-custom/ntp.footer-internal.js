// ===============================================================
// Show Internal Footer Links (requires ntp.common.js & jQuery)
// ===============================================================
$(document).ready(function(){
	
	//add "NTP Staff" links if inside the network
	$.get(NTP.PublicSiteHostName + '/inside.cfm', function (data) {
		if (data != "") {
			var $data = $(data);
			$("#footer-ntp").after($data);

			//get page URL for "Request an Update to this Page"
			var pageURL = encodeURIComponent(window.location.href);
			
			//append page URL to the "Request an Update to this Page" link
			var requestUpdateLink = $($data.find('a[href*="webforms"]'));
			var updateForm = requestUpdateLink.attr('href');
			requestUpdateLink.attr('href', updateForm + '&webpage=' + pageURL);
		}
	}, 'html'); 

});