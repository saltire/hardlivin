$(function() {
	
	var width = 6;
	var height = 5;
	
	// build board to specified dimensions
	for (y = 0; y < height; y++) {
		$row = $('<div />').appendTo('.board');
		for (x = 0; x < width; x++) {
			$row.append($('<div class="square" />').append('<a />'));
		}
	}
	
	// load square names into an array
	var sqids = [];
	$('.squares span').each(function() {
		sqids.push($(this).attr('id'));
	});
	$('.squares').remove();

	var squares = [];
	// find half as many squares as there are spots on the board
	for (i = 0; i < width * height; i += 2) {
		var addsq = false;
		
		// pick random squares until we find an unused one
		while (!addsq) {
			var sqi = Math.floor(Math.random() * sqids.length);
			var sqid = sqids[sqi];
			if (squares.indexOf(sqid) == -1) {
				
				// add the square to the array twice
				for (j = 0; j < 2; j++) {
					var addpos = false;
					
					// pick random positions until we find a vacant one
					while (!addpos) {
						var pos = Math.floor(Math.random() * width * height);
						if (squares[pos] == undefined) {
							squares[pos] = sqid;
							addpos = true;
						}
					}
				}
				addsq = true;
			}
		}
	}
	
	$('.board a').click(function() {
		if ($('img', this).length || $('.active').length == 2) {
			return;
		}
		
		var pos = $('.board a').index($(this));
		
		// get id of unmatched face-up square, if any
		var otherid = $('.active').length ? $('.active').first().attr('data-name') : null;
		
		// turn off clickable appearance for all squares if two have been flipped over
		if (otherid !== null) {
			$('.board a').addClass('noclick');
		}
		
		// animate it to 0 width
		$(this).addClass('noclick').animate({width: 0}, 100, function() {
			// now that it's invisible, append the image
			$('<img src="static/images/128/' + squares[pos] + '.png" />')
				.attr('data-name', squares[pos]).addClass('active').appendTo($(this));
			// now animate it back to full width
			$(this).animate({width: $(this).css('height')}, 100, function() {
				if (otherid == null) {
					return;
				}
				
				// increment turn counter
				$('.turns').html(parseInt($('.turns').html()) + 1);
				
				// match: keep both squares
				if (otherid == squares[pos]) {
					$('<div class="overlay" />').insertAfter($('.active').parent())
						.css({background: '#0f0'}).fadeOut(750);
					$('.active').removeClass('active').parent().addClass('solved');
					$('.board a:not(.solved)').removeClass('noclick');
				}
				// no match: remove both squares
				else {
					window.setTimeout(function() {
						$('.active').parent().animate({width: 0}, 100, function() {
							$('.active').remove();
							$(this).animate({width: $(this).css('height')}, 100, function() {
								$('.board a:not(.solved)').removeClass('noclick');
							});
						});
					}, 500);
				}
			});
		})
	});
});
