$(function() {
	$('select').prop('selectedIndex', 0);
	
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
			var col = $(this).siblings('.col').val();
			var row = $(this).siblings('.row').val();
			if (col == '-' || row == '-') {
				return;
			}
			info[$(this).attr('id').slice(7)] = {
				sold: 0,
				srow: 'ABCDE'.indexOf(row),
				scolumn: parseInt(col) - 1
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