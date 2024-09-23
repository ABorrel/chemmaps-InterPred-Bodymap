// ===============================================================
// Footer (requires jQuery, ntp.common.js, & Foundation MediaQuery)
// ===============================================================
$(document).ready(function(){

	function footerMobile() {
		$('.link-category ul').hide();
		$('.link-category h5').unbind('click keyup').attr("tabindex", "0").on({
			click: function() {
				$(this).next('ul').slideToggle();
				$(this).toggleClass('footer-nav-active');
			},
			keyup: function(event) {
				if(event.keyCode == 13){
					$(this).click();
				}
			}			
		});
	}	
	function footerDesktop() {
		$('.link-category h5').removeAttr("tabindex").off('click keyup');
		$('.link-category ul').show();
	}
	
	//trigger at breakpoint
	onFooterMobile = function() {
		if (Foundation.MediaQuery.is('small only')) {
			footerMobile();
		} else {
			footerDesktop();
		}
	}
	
	//on page load and media query change, initialize onFooterMobile();
	$(window).on('load changed.zf.mediaquery', onFooterMobile);
	
	//add title attribute to external links in the footer
	$('#footer a.external, .footer-logos a').attr('title', ntpExternalDisclaimer);

});