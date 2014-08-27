jQuery( document ).ready(function( $ ) {
	console.info('Question.js loaded')
	$('button[name=loadstats]').click(function(evt){
		evt.preventDefault()
		$.colorbox({
			href:"statistics.html",
			scrolling: false,
			transition: "fade",
			onComplete: function(){ $.colorbox.resize() }
		});
		return false
	})
})