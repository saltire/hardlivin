$(function() {
	
	var width = 6;
	var height = 5;
	
	// build board to specified dimensions
	for (y = 0; y < height; y++) {
		$row = $('<div />').appendTo('.board');
		for (x = 0; x < width; x++) {
			$row.append('<div><a /></div>');
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
		
		if (otherid !== null) {
			$('.board a').css({cursor: 'default'});
		}
		
		// turn over this square
		$(this).animate({width: 0}, 100, function() {
			console.log($(this));
			$('<img src="./static/images/64/' + squares[pos] + '.png" />')
				.attr('data-name', squares[pos]).addClass('active').appendTo($(this));
			$(this).animate({width: $(this).css('height')}, 100);

			// match: keep both squares
			if (otherid == squares[pos]) {
				$('.active').removeClass('active');
				$('.board a').css({cursor: 'pointer'});
			}
			// no match: remove both squares
			else if (otherid !== null) {
				window.setTimeout(function() {
					$('.active').parent().animate({width: 0}, 100, function() {
						$('.active').remove();
						$(this).animate({width: $(this).css('height')}, 100, function() {
							$('.board a').css({cursor: 'pointer'});
						});
					});
				}, 1000);
			}
		})
	});
});
