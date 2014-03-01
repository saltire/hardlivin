$(function() {
	
	// dim sold squares with checkbox
	
	$('#dim-sold').prop('checked', false).change(function() {
		$sold = $('.sold input:checked').map(function() {
			return $('.square[href$="' + $(this).closest('.info > div').attr('id') + '"]');
		}).toggleClass('dimmed');
		console.log($sold);
	});
	
	
	// sold checkbox toggles dim on the corresponding square if that option is enabled
	
	$('.sold input').change(function() {
		if ($('#dim-sold').is(':checked')) {
			$('.square[href$="' + $(this).closest('.info > div').attr('id') + '"]')
				.toggleClass('dimmed');
		}
	});
	
	
	// dim non-snakes squares with checkbox
	
	$('#dim-snakes').prop('checked', false).change(function() {
		$snakes = $('.notsnakes input:checked').map(function() {
			return $('.square[href$="' + $(this).closest('.info > div').attr('id') + '"]');
		}).toggleClass('dimmed');
		console.log($snakes);
	});
	
	
	// snakes checkbox toggles dim on the corresponding square if that option is enabled
	
	$('.notsnakes input').change(function() {
		if ($('#dim-snakes').is(':checked')) {
			$('.square[href$="' + $(this).closest('.info > div').attr('id') + '"]')
				.toggleClass('dimmed');
		}
	});
	
	
	// options add changed flag to their items and enable save button
	
	$('.sold, .locked, .notsnakes, .difficulty').find('input').change(function() {
		$(this).closest('.info > div').attr('data-changed', 1);
		$('.save').removeClass('disabled');
	});

	
	// reset difficulty checkboxes
	
	$('.difficulty input[checked="true"]').prop('checked', true);
	
	
	// click squares to show their info
	
	$('.board, .unused').on('click', '.square', function(e) {
		e.preventDefault();
		$('.info > div').hide();
		$('.info #' + $(this).attr('href').slice(1)).show();
	});
	
	
	// edit name and description of square in info area
	
	$('.info .title, .info .desc, .info .effect').editable({
		lineBreaks: false,
		callback: function(data) {
			if (data.$el.hasClass('title') && data.content == '') {
				// reset content of title if it is blank
				data.$el.html(data.$el.attr('data-original'));
				
			} else if (data.content !== false) {
				// add changed flag to this item and enable save button
				data.$el.closest('.info > div').attr('data-changed', 1);
				$('.save').removeClass('disabled');
			}
			data.$el.removeAttr('data-original');
		},
	}).on('edit', function(e, $el) {
		$el.parent().attr('data-original', $el.val());
	});
	
	
	// save board to csv
	
	$('.save').click(function(e) {
		e.preventDefault();
		if ($(this).hasClass('disabled')) {
			return;
		}
		
		// collect name and description of each
		var info = {};
		$('.info > div').each(function() {
			var row = '', column = '';
			var $boardsq = $('.board .square[href$=' + $(this).attr('id') + ']');
			if ($boardsq.length) {
				row = $boardsq.index();
				column = $('.column').length - $boardsq.parent().index();
				if (!$('.column:first .square').length) {
					column -= 1;
				}
			}
			info[$(this).attr('id')] = {
				title: $('.title', this).text(),
				desc: $('.desc', this).text(),
				effect: $('.effect', this).text(),
				difficulty: $('.difficulty input:checked', this).val(),
				locked: $('.locked input', this).is(':checked') ? 1 : 0,
				sold: $('.sold input', this).is(':checked') ? 1 : 0,
			};
			if ($('.board.hashtag').length) {
				$.extend(info[$(this).attr('id')], {
					column: column,
					row: row,
					snakes: !$('.notsnakes input', this).is(':checked') ? 1 : 0,
				});
			} else if ($('.board.snakes').length) {
				$.extend(info[$(this).attr('id')], {
					scolumn: column,
					srow: row,
				});
			}
		});
		
		$.ajax({
			type: 'POST',
			contentType: 'application/json',
			data: JSON.stringify(info),
			url: '/configurator/save',
			success: function(e) {
				$('<span />').appendTo('.status').html('Saved!').css({color: '#0f0'}).fadeOut(2000);
				$('.save').addClass('disabled');
			},
		});
	});
});