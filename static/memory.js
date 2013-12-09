$(function() {
	
	var width = 6;
	var height = 5;
	
	for (y = 0; y < height; y++) {
		$row = $('<div />').appendTo('.game');
		for (x = 0; x < width; x++) {
			$row.append('<a />');
		}
	}

	var squares = [];
	for (i = 0; i < width * height / 2; i++) {
		while (squares.length == i) {
			var sq = Math.floor(Math.random() * $('.squares img').length);
			if (squares.indexOf(sq) == -1) {
				squares.push(sq);
			}
		}
	}
	
	for (i in squares) {
		var $img = $('.squares img').eq(squares[i]);
		for (i = 0; i < 2; i++) {
			var placed = false;
			while (!placed) {
				var r = Math.floor(Math.random() * width * height);
				if ($('.game a').eq(r).is(':empty')) {
					$img.clone().appendTo($('.game a').eq(r));
					placed = true;
				}
			}
		}
	}
	
});
