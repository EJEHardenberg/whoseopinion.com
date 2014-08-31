jQuery( document ).ready(function( $ ) {
	console.info('Question.js loaded')
	var sideScreenShowing = false
	$('html').click(function(event){
		if(!$(event.target).closest('article').length) {
			if(sideScreenShowing){
				$('article').animate({left: '100vw'}, 500, function(){
					sideScreenShowing = false
				})
			}
		}
	})
	$('button[name=loadstats]').click(function(evt){
		evt.preventDefault()
		$.get("info.html", function(e){
			$('article div').html(e)
			showMap()
			$('article').animate({left: "50vw", },500, function(){
				sideScreenShowing = true	
			})
		})
		return false
	})
	$('span[name=vote-help]').tooltipster({
		contentAsHTML: true,
		content: $('#vote-help').html(),
		position: "bottom"
	})
})