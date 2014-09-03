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
	$('form[name=question]').submit(function(evt){
		/* Submit Question via AJAX so that we don't lose the page. */
		evt.preventDefault()
		console.debug("Form Submit")
		$.ajax({
			data: $(this).serialize(),
			url: $(this).attr('action'),
			type: $(this).attr('method'),
			context: this,
			success: function(response){
				/* Do something or another */
				var btn = $(this).find('button[name=vote]')
				btn.attr('name','showscale')
				btn.text('Voice yours')
				$(this).find('section').slideToggle()
			},
			error: function(){
				alert("There was a problem submitting your form")
			}
		})
		return false
	})
})