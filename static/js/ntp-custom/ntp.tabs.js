// ===============================================================
// Tabs (requires jQuery)
// ===============================================================
function ntpTabs() {

	//disable tab functionality where needed
	$('[data-tabs] > li').each(function() {
		var nextTab = $(this).next();
		var prevTab = $(this).prev();
		
		if ($(this).is(':first-child')) {
			prevTab = $(this).parent().find('li:last-child');
		}
		if ($(this).is(':last-child')) {
			nextTab = $(this).parent().find('li:first-child');
		}

		if ($(nextTab).hasClass('disabled')) {
			$(this).find('a').on('keydown', function(e) {
				if (e.keyCode == 39 || e.keyCode == 40 || e.keyCode == 98 || e.keyCode == 102) {
					e.preventDefault();
					e.stopImmediatePropagation();
					e.stopPropagation();
				}
			});
		}
		if ($(prevTab).hasClass('disabled')) {
			$(this).find('a').on('keydown', function(e) {
				if (e.keyCode == 37 || e.keyCode == 38 || e.keyCode == 100 || e.keyCode == 104) {
					e.preventDefault();
					e.stopImmediatePropagation();
					e.stopPropagation();
				}
			});
		}
	});

	$('[data-tabs] > li.disabled a, .meeting-registration.disabled a').each(function() {
		$(this).on('click focus keydown', function(e) {
			e.preventDefault();
			e.stopImmediatePropagation();
			e.stopPropagation();
		});
	});

}

$(document).ready(function(){
	ntpTabs();
});