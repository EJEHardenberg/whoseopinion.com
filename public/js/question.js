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
	$(document).on('click', 'button[name=loadstats]',function(evt){		
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

	

	$(document).on('submit','form[name=question]',function(evt){
		/* Submit Question via AJAX so that we don't lose the page. */
		evt.preventDefault()
		console.debug("Form Submit")
		$.ajax({
			data: $(this).serialize(),
			url: $(this).attr('action'),
			type: $(this).attr('method'),
			context: this,
			beforeSend: function(xhr, settings){
				if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             		// Only send the token to relative URLs i.e. locally.
             		console.debug('set token')
             		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         		}
			},
			success: function(response){
				/* Do something or another */
				var btn = $(this).find('button[name=vote]')
				btn.attr('name','showscale')
				btn.text('Voice yours')
				$(this).find('section').slideToggle()
				$.colorbox({
					overlayClose: true,
					closeButton: false,
					html: $(this).find('[rel=success]').html()
				})
				setTimeout($.colorbox.close,1250)
			},
			error: function(){
				alert("There was a problem submitting your form")
			}
		})
		return false
	})
})

function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}


	function getAuthFromApi(){
		var url = window.apiuri + "auth"
		$.ajax({
			url: url,
			type: "GET",
			success: function(response){
				console.info("Heartbeat made", response)
			},
			error: function(e){
				if(e.status != 200){
					alert("Could not hear heartbeat of webserver")
					console.error(e)
				}
			}
		})
	}	