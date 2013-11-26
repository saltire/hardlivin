$(function() {
	
	// count columns after the board changes, to ensure there is one blank column at the end
	
	function setEmptyColumns() {
		var $emptycols = $('.board .square').last().parent().nextAll();
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
			var $lastcol = $('<div class="column" />').appendTo('.board');
			for (i = 0; i < 5; i++) {
				$('<div class="empty" />').droppable(drop_opts).appendTo($lastcol);
			}
		}
		$('.board').css({minWidth: $('.column').length * $('.column').outerWidth(true) + 'px'});
	}
	
	
	// click squares to show their info
	
	$('.board, .unused').on('click', '.square', function() {
		$('.info > div').hide();
		$('.info #' + $(this).attr('href').slice(1)).show();
		return false;
	});
	
	
	// edit name and description of square in info area
	
	//$('.info p').editable({ // changing square names not supported yet
	$('.info .desc').editable({
		lineBreaks: false,
		callback: function(data) {
			if (data.$el.hasClass('name') && data.content == '') {
				// reset content of title if it is blank
				data.$el.html(data.$el.attr('data-original'));
				
			} else if (data.content !== false) {
				data.$el.attr('data-changed', 1);
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
	
	$('.save').click(function() {
		if ($(this).hasClass('disabled')) {
			return false;
		}
		
		// collect columns in the board
		var columns = [];
		$('.column').slice(0, -1).each(function() {
			var column = [];
			$(this).children().each(function() {
				column.push($(this).hasClass('square') ? $(this).attr('href').slice(1) : '');
			});
			columns.push(column.join(','));
		});
		
		// collect name and description of each
		var info = {};
		$('.info p[data-changed=1]').removeAttr('data-changed').parent().each(function() {
			info[$(this).attr('id')] = {
				name: $('.name', this).text(),
				desc: $('.desc', this).text(),
			};
		});
		
		$.ajax({
			type: 'POST',
			contentType: 'application/json',
			data: JSON.stringify({columns: columns, info: info}),
			url: 'save',
			success: function(e) {
				$('.status').css({color: '#0f0'}).html('Saved!').fadeOut(2000);
				$('.save').addClass('disabled');
			},
		});
	});
});