$(function() {
	
	// click squares to show their info
	
	$('.board .square').click(function(e) {
		e.preventDefault();
		$('.info > div').hide();
		$('.info #' + $(this).attr('href').slice(1)).show();
	});
	
});