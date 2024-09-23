// ===============================================================
// Modal (requires jQuery, jQueryUI, Foundation Reveal, & Foundation MediaQuery))
// ===============================================================	
$(document).ready(function() {

	//add keyboard-accessible toggle to all Foundation Reveal instances
	$('[data-open]').each(function () {
		$(this).attr('title', 'Open modal window for ' + $(this).text()).on({
			keydown: function(event) {
				if (event.keyCode == 13) {
					$(this).click();
				}
			}
		});
	});

	//add functionality for image, iframe, and AJAX modals
    $('.modal-image, .modal-iframe, .modal-ajax').each(function () {

        //define modal source
        if ($(this).is('a')) {
			var modalTarget = $(this);
        } else {
			var modalTarget = $(this).find('a');
        }
		
		var modalContent = modalTarget.attr('href');
        var modalTitle = $(this).attr('data-title');
        var modalExternal = $(this).attr('data-external');
        var modalCaption = $(this).attr('data-caption');
        var modalAlt = $(this).attr('data-alt');
        var modalTableId = $(this).attr('data-tableid');
        var modalSize = $(this).attr('data-size');
        var modalWidth = $(this).attr('data-width');
        var modalHeight = $(this).attr('data-height');

        //generate modal window
		$('<div class="reveal" aria-label="Modal Window"><div class="reveal-caption"></div><button class="close-button" data-close aria-label="Close Modal" type="button"><span class="fa fa-close" aria-hidden="true"></span></button></div>').insertAfter($(this)).uniqueId();

		//initialize Foundation Reveal
		var thisId = $(this).next('.reveal').attr('id');
		var $modalId = $('#' + thisId);
		var $modalInit = new Foundation.Reveal($modalId);

		//populate and customize modal window by type
        if ($(this).hasClass('modal-image')) {
			//image modal
			$(modalTarget).attr('title', 'Open Expanded Image')
			$modalId.addClass('image').attr('aria-label', 'Expanded Image').prepend('<div class="reveal-image"><img src="' + modalContent + '" alt="' + modalAlt + '"></div>');
		}
        if ($(this).hasClass('modal-iframe')) {
			//iFrame modal
			$modalId.addClass('iframe').prepend('<div class="modal-content"><iframe src="' + modalContent + '"></iframe></div>');
			$modalId.on('open.zf.reveal', function() {
				ntpVideo();
			});
        }
        if ($(this).hasClass('modal-ajax')) {
			//AJAX modal
			$modalId.addClass('ajax').prepend('<div class="ajax-content">Loading...</div>');
			$modalId.on('open.zf.reveal', function () {
				if (modalExternal === 'true') {
					$modalId.find('.ajax-content').load(modalContent, function () {
						$modalId.find('.ajax-content').foundation();
					});
				} else {
					$modalId.find('.ajax-content').load(modalContent + ' #pagecontent', function () {
						$modalId.find('.ajax-content #pagecontent').attr('class', 'columns small-12').uniqueId().foundation();
						createTableOfContents();
						ntpFormValidation();
						ntpModalExternalLinks();
						ntpModalProgressiveDisclosure();
						ntpSlider();
						ntpTables();
						ntpTabs();
						ntpTooltip();
						ntpVideo();
					});
				}
			});
		}

		//populate caption
		if (modalCaption !== undefined && modalCaption !== false) {
			$modalId.find('.reveal-caption').html('<p>' + modalCaption + '</p>');
		}

        //define size of modal
        if (modalSize === 'tiny') {
            $modalId.addClass('tiny');
        } else if (modalSize === 'small') {
            $modalId.addClass('small');
        } else if (modalSize === 'large') {
            $modalId.addClass('large');
        } else if (modalSize === 'full') {
            $modalId.addClass('full');
			$modalId.on('open.zf.reveal', function() {
			   $(this).css('top', '0');
			});
        } else {
            $modalId.addClass('small');
        }

        //custom size on initialization for desktop and tablet
        if (Foundation.MediaQuery.atLeast('medium')) {
            if (modalWidth !== undefined && modalWidth !== false) {
                $modalId.css('width', modalWidth);
            }
            if (modalHeight !== undefined && modalHeight !== false) {
                $modalId.css('height', modalHeight);
            }
        }

        //toggle custom size at breakpoint
        $(window).on('changed.zf.mediaquery', function () {
			//store top positioning
			$modalId.data('top', $modalId.css('top'));
            if (Foundation.MediaQuery.is('small only')) {
                $modalId.css({
                    'width': '100%',
                    'height': '100%'
                });
                //remove top positioning
                $modalId.css('top', '0');
            } else {
                if (modalWidth !== undefined && modalWidth !== false) {
                    $modalId.css('width', modalWidth);
                }
                if (modalHeight !== undefined && modalHeight !== false) {
                    $modalId.css('height', modalHeight);
                }
                //restore top positioning
                $modalId.css('top', $modalId.data('top'));
            }
        });

        //populate ARIA labels & titles
        if (modalTitle !== undefined && modalTitle !== false) {
            $(modalTarget).attr('title', 'Open ' + modalTitle + ' Modal');
            $modalId.attr('aria-label', modalTitle);
            $modalId.find('.close-button').attr('aria-label', 'Close ' + modalTitle + ' Modal');
        } else {
            $(this).attr('title', 'Open Modal Window for ' + $(this).text());
        }

        //add dynamic trigger
        $(modalTarget).attr({
            'id': 'link-' + thisId,
            'aria-haspopup': true,
            'data-open': thisId,
            'tabindex': '0'
        }).on({
            click: function (e) {
                e.preventDefault();
                $modalId.foundation('open');
            },
            keydown: function (e) {
                if (e.keyCode == 13) {
                    $(this).click();
                }
            }
		});

        //return focus after close
        $modalId.on('closed.zf.reveal', function () {
            $('#link-' + thisId).focus();
        });

    });

});