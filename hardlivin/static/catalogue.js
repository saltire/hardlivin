$(function() {
	$('html, body').prop('scrollTop', 0);
	$('select').prop('selectedIndex', 0);
	
	$('.catalogue h2').click(function() {
		$(this).next().slideToggle('slow');
	});
	
	$('.chart table img').click(function() {
		var $entry = $('.list img[src="' + $(this).attr('src') + '"]');
		$entry.closest('.list').show();
		$('html, body').animate({
			scrollTop: $entry.offset().top
		}, 'slow');
	});
	
	$('input').click(function(e) {
		e.preventDefault;
		
		var info = {};
		
		if ($(this).hasClass('sell')) {
			info[$(this).attr('id').slice(5)] = {
				sold: 1,
				srow: '',
				scolumn: ''
			};
		}
		else if ($(this).hasClass('unuse')) {
			info[$(this).attr('id').slice(6)] = {
				sold: 0,
				srow: '',
				scolumn: ''
			};
		}
		else if ($(this).hasClass('moveto')) {
			var pos = $(this).prev().val();
			if (pos == '-') {
				return;
			}
			var coords = pos.split(',');
			info[$(this).attr('id').slice(7)] = {
				sold: 0,
				srow: parseInt(coords[1]),
				scolumn: parseInt(coords[0])
			};
		}
		
		$('input').off('click').addClass('disabled');
		
		$.ajax({
			type: 'POST',
			contentType: 'application/json',
			data: JSON.stringify(info),
			url: '/configurator/save',
			success: function(e) {
				window.location.reload();
			},
		});
	});
	
});