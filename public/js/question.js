jQuery( document ).ready(function( $ ) {
	console.info('Question.js loaded')
	$('button[name=loadstats]').click(function(evt){
		evt.preventDefault()
		$.colorbox({
			href:"statistics.html"
		});
		return false
	})
})