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
			if(typeof showMap == 'function'){
				showMap($)
			}
			$('article').animate({left: "50vw", },500, function(){
				sideScreenShowing = true	
			})
		})
		return false
	})
	$(document).on('click', 'button[name=showscale]', function(evt){
		var section = $(this).closest('form').find('section')
		section.slideToggle()
		$(this).attr('name','vote')
		$(this).text('Vote')
		return false
	})
})