$(function() {
	
	function setEmptyColumns() {
		var $emptycols = $('.column .square').last().parent().nextAll();
		if ($emptycols.length > 1) {
			// remove all but one empty column from the end 
			$emptycols.slice(1).remove();
		}
		else if ($emptycols.length == 0) {
			// add one empty column to the end
			var $lastcol = $('<div class="column" />').appendTo('.board');
			for (i = 0; i < 5; i++) {
				$('<div class="empty" />').droppable(drop_opts).appendTo($lastcol);
			}
		}
		$('.board').css({minWidth: $('.column').length * $('.column').outerWidth(true) + 'px'});
	}
	
	var drag_opts = {
		connectToSortable: '.unused',
		helper: 'clone',
		appendTo: 'body',
		revert: 'invalid',
		start: function(e, ui) {
			$(this).trigger('click');
			$(this).addClass('ui-dragged');
		},
		stop: function(e, ui) {
			$(this).removeClass('ui-dragged');
		},
	};
	
	var drop_opts = {
		hoverClass: 'ui-drophover',
		drop: function(e, ui) {
			// create clone of square to add at drop spot
			var $sq = ui.helper.clone().removeClass('ui-draggable-dragging').removeClass('ui.dragged')
				.draggable(drag_opts).css({position: 'relative', top: 'auto', left: 'auto'});
			
			if (ui.draggable.parent().hasClass('column')) {
				// if moved from board, replace with a blank square
				ui.draggable.replaceWith($('<div class="empty" />').droppable(drop_opts));
				
			} else {
				// if moved from unused area, remove it
				ui.draggable.remove();
			}
			
			// add the clone we created
			$(this).replaceWith($sq);
			
			setEmptyColumns();
			
			$('.save').removeClass('disabled');
		},
	};
	
	$('.board, .unused').on('click', '.square', function() {
		// show the square in the info area
		$('.info > div').hide();
		$('.info #' + $(this).attr('href').slice(1)).show();
		return false;
	});
	
	$('.board .square').draggable(drag_opts);
	
	$('.empty').droppable(drop_opts);
	
	$('.unused').sortable({
		start: function(e, ui) {
			ui.item.trigger('click');
		},
		receive: function(e, ui) {
			if (ui.item.parent().hasClass('column')) {
				// if moved from board, replace with a blank square
				ui.item.after($('<div class="empty" />').droppable(drop_opts)).detach();
				setEmptyColumns();
			}
		},
		update: function(e, ui) {
			ui.item.removeClass('ui-dragged');
		},
	});
	
	$('.save').click(function() {
		if ($(this).hasClass('disabled')) {
			return false;
		}
		
		var columns = [];
		$('.column').slice(0, -1).each(function() {
			var column = [];
			$(this).children().each(function() {
				column.push($(this).hasClass('square') ? $(this).attr('href').slice(1) : '');
			});
			columns.push(column.join(','));
		});
		
		$.post('save', {columns: columns}, function(response) {
			$('.status').css({color: '#0f0'}).html('Saved!').fadeOut(2000);
			$('.save').addClass('disabled');
		});
	});
});