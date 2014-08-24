jQuery( document ).ready(function( $ ) {
	console.info('Question.js loaded')
	$('button[name=loadstats]').click(function(){
		$.colorbox({
			href:"statistics.html"
		});
	})
})