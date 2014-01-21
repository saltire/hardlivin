function colourRandomLetter() {
	var $nohover = $('.title div').not('.hover');
	var random = Math.floor(Math.random() * $nohover.length);
	$('.hover').removeClass('hover');
	$nohover.eq(random).addClass('hover');
	setTimeout(colourRandomLetter, 300);
}

$(function() {
	$('.title div').click(function() {
		$('.title div').off();
		colourRandomLetter();
	});
});
