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
	$('span[name=vote-help]').tooltipster({
		contentAsHTML: true,
		content: $('#vote-help').html(),
		position: "bottom"
	})
	$('span[name=more-info]').click(function(){
		$.get("question-info.html", function(e){
			$('section[name=information]').html(e)	
		})
		
	})
})