$(function() {
	
	// count columns after the board changes, to ensure there is one blank column at the end
	
	function setEmptyColumns() {
		var $emptycols = $('.column .square:not(".ui-dragged")').first().parent().prevAll();
		if ($emptycols.length > 1) {
			// remove all but one empty column from the end
			$emptycols.slice(1).remove();
		}
		else if ($emptycols.length == 0) {
			// if no squares on the board at all, clear all columns
			if ($('.board .square').length == 0) {
				$('.board').empty();
			}
			// add one empty column to the end
			var $lastcol = $('<div class="column" />').prependTo('.board');
			for (i = 0; i < 5; i++) {
				$('<div class="empty" />').droppable(drop_opts).appendTo($lastcol);
			}
		}
		$('.board').css({minWidth: $('.column').length * $('.column').outerWidth(true) + 'px'});
		
		// recalculate square count for each area
		$('.bcount').html($('.board .square').length);
		$('.ucount').html($('.unused .square').length);
		
		// set clear and random buttons
		$('.clear').toggleClass('disabled', !$('.board .square').length);
		$('.random').toggleClass('disabled', !$('.unused .square').length);
	}
	
	// dim painted squares with checkbox
	
	$('#dim-painted').prop('checked', false).change(function() {
		$painted = $('.painted input:checked').map(function() {
			return $('.square[href$="' + $(this).closest('.info > div').attr('id') + '"]');
		}).toggleClass('dimmed');
		console.log($painted);
	});
	
	
	// options add changed flag to their items and enable save button
	
	$('.painted, .locked, .difficulty').find('input').change(function() {
		$(this).closest('.info > div').attr('data-changed', 1);
		$('.save').removeClass('disabled');
	});

	
	// painted checkbox toggles dim on the corresponding square if that option is enabled
	
	$('.painted input').change(function() {
		if ($('#dim-painted').is(':checked')) {
			$('.square[href$="' + $(this).closest('.info > div').attr('id') + '"]')
				.toggleClass('dimmed');
		}
	});
	
	
	// reset difficulty checkboxes
	
	$('.difficulty input[checked="true"]').prop('checked', true);
	
	
	// clear board
	
	$('.clear').click(function(e) {
		e.preventDefault();
		if ($(this).hasClass('disabled')) {
			return;
		}
		
		$('.board .square').filter(function() {
			return $('.locked input', $(this).attr('href')).not(':checked').length;
		}).after($('<div class="empty" />').droppable(drop_opts))
			.draggable('destroy').appendTo('.unused');
		setEmptyColumns();
	});
	
	
	// fill board randomly
	
	$('.random').click(function(e) {
		e.preventDefault();
		if ($(this).hasClass('disabled')) {
			return;
		}
		
		// add empty columns if necessary
		while ($('.unused .square').length > $('.empty').length) {
			var $lastcol = $('<div class="column" />').prependTo('.board');
			for (var s = 0; s < 5; s++) {
				$('<div class="empty" />').appendTo($lastcol);
			}
		}
		
		// get unused squares of each level, and find the # of columns needed for each level
		var $unleveled = $('.unused .square'),
			leveled = [],
			levelempty = [];
		for (var i = 0; i < 5; i++) {
			leveled[i] = $unleveled.filter(function() {
				return 5 - parseInt($('.difficulty input:checked', $(this).attr('href')).val()) == i;
			});
			$unleveled = $unleveled.not(leveled[i]);
			
			// get empty squares at this level
			levelempty[i] = $('.empty').filter(function() {
				return $(this).index() == i;
			});
			
			// add empty columns at this level if necessary
			while (leveled[i].length > levelempty[i].length) {
				var $lastcol = $('<div class="column" />').prependTo('.board');
				for (var s = 0; s < 5; s++) {
					$('<div class="empty" />').appendTo($lastcol);
				}
				levelempty[i] = levelempty[i].add($('.empty', $lastcol).eq(i));
			}
		}
		
		// place squares for each level
		for (var i = 0; i < 5; i++) {
			while (leveled[i].length) {
				var $square = leveled[i].eq(Math.floor(Math.random() * leveled[i].length));
				var $empty = levelempty[i].eq(Math.floor(Math.random() * levelempty[i].length));
				$empty.replaceWith($square.draggable(drag_opts));
				leveled[i] = leveled[i].not($square);
				levelempty[i] = levelempty[i].not($empty);
			}
		}
		
		// place unleveled squares
		while ($unleveled.length) {
			var $square = $unleveled.eq(Math.floor(Math.random() * $unleveled.length));
			var $empty = $('.empty').eq(Math.floor(Math.random() * $('.empty').length));
			$empty.replaceWith($square.draggable(drag_opts));
			$unleveled = $unleveled.not($square);
		}
		
		$('.empty').droppable(drop_opts);
		setEmptyColumns();
	});
	
	
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
	
	
	// drag and drop between board, and sortable unused squares
	
	var drag_opts = {
		connectToSortable: '.unused',
		helper: 'clone',
		appendTo: 'body',
		revert: 'invalid',
		start: function(e, ui) {
			// trigger click to show info
			$(this).trigger('click');
			
			// add css class to style original square during drag
			$(this).addClass('ui-dragged');
		},
		stop: function(e, ui) {
			// remove class in case drag was incomplete
			$(this).removeClass('ui-dragged');
			
			// if dropped elsewhere on the board, replace with a droppable blank square
			if (ui.helper.attr('data-dropped')) {
				ui.helper.removeAttr('data-dropped');
				$(this).replaceWith($('<div class="empty" />').droppable(drop_opts));
			}
		},
	};
	$('.board .square').draggable(drag_opts);
	
	var drop_opts = {
		hoverClass: 'ui-drophover',
		drop: function(e, ui) {
			// if moved from unused area, remove it from there
			if (ui.draggable.parent().hasClass('unused')) {
				ui.draggable.remove();
			}
			
			// replace with a clone of the dragged helper, clear css and bind events
			$(this).replaceWith(ui.helper.clone().removeClass('ui-draggable-dragging')
				.css({position: 'relative', top: 'auto', left: 'auto'}).draggable(drag_opts));
			
			// add a flag to the helper so we know to replace the original with a blank
			ui.helper.attr('data-dropped', 1);
			
			setEmptyColumns();
			
			$('.save').removeClass('disabled');
		},
	};
	$('.empty').droppable(drop_opts);
	
	$('.unused').sortable({
		scroll: false,
		start: function(e, ui) {
			ui.item.trigger('click');
		},
		receive: function(e, ui) {
			// if dragged from the board, replace original with a droppable blank square
			if (ui.item.parent().hasClass('column')) {
				ui.item.after($('<div class="empty" />').droppable(drop_opts)).detach();
				setEmptyColumns();
			}
		},
		update: function(e, ui) {
			ui.item.removeClass('ui-dragged');
		},
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
				column = $('.column').length - $boardsq.parent().index() - 1;
			}
			info[$(this).attr('id')] = {
				title: $('.title', this).text(),
				desc: $('.desc', this).text(),
				effect: $('.effect', this).text(),
				difficulty: $('.difficulty input:checked', this).val(),
				column: column,
				row: row,
				locked: $('.locked input', this).is(':checked') ? 1 : 0,
			};
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