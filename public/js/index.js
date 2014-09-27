jQuery( document ).ready(function( $ ) {
	console.info("Index.js loaded")	

	var loadQuestionsEvent = "load_questions"
	var popularCategoryFlag = -1

	loadedQuestionsCache = {}

	/* First, load the categories */
	function catHandler(json){
		/* Check that it's an array first */
		if(!(json instanceof Array)){
			alert("Could not load categories.")
			return;
		}

		var ul = $('#category-list')
		for (var i = json.length - 1; i >= 0; i--) {
			var li = document.createElement("li")
			var anchor = document.createElement("a")
			$(anchor).text(json[i].cat_name)
			$(anchor).attr('href', '/#category-list:' + json[i].id)
			$(anchor).attr('rel', json[i].id)
			$(li).append(anchor)
			$(li).hide()
			  ul.append(li)
			$(li).fadeIn()
		};
		/* Fire the event handler to load popular questions */
		$.event.trigger({
			type: loadQuestionsEvent,
			category: popularCategoryFlag
		})
	}
	$.getJSON(window.apiuri + "categories/", catHandler)

	

	function displayQuestions(json){
		//json is list of objects
		console.log('displayQuestions',json)
		$('#questions').find('.question').remove()
		loadedQuestionsCache[loadedQuestionsCache['newest']] = json
		for (var i = json.length - 1; i >= 0; i--) {
			var q = json[i]
			var categoryText = $('#category-list a[rel='+q.category+']').text()
			var qView = makeQuestion(categoryText, q.statement, q.id)
			$('#questions').append(qView)
		};

	}

	function loadQuestions(e){
		console.log('loadQuestions', e.category)
		var categoryId = parseInt(e.category)
		if(isNaN(categoryId)){
			console.debug("Invalid category id being passed to function")
			return
		}
		var url = window.apiuri +  'category/' + categoryId + '/'
		loadedQuestionsCache['newest'] = url //this is how we pass the info to the function that will cache
		if(url in loadedQuestionsCache){
			console.debug('Using cached copy of data', url)
			displayQuestions(loadedQuestionsCache[url])
		}else{
			$.getJSON(url, displayQuestions)
		}
	}
	$('#category-list').on('click', 'a', function(evt){
		var id = $(this).attr('href').split(':')[1]
		$.event.trigger({
			type: loadQuestionsEvent,
			category: id
		})
	})

	$(document).on(loadQuestionsEvent, loadQuestions)

	function makeQuestion(category, text, id){
		var qWrapper = document.createElement('div')
		$(qWrapper).addClass('question')
		$(qWrapper).append(
			$(document.createElement('div')).text(category)
			)
		$(qWrapper).append(
			$(document.createElement('p')).text(text)
			)
		var form = document.createElement('form')
		var hiddenInput = document.createElement('input')
		$(hiddenInput).attr('type', 'hidden')
		$(hiddenInput).attr('value', id)
		$(hiddenInput).attr('name','question')
		$(form).append( hiddenInput )
		$(form).attr('method', 'POST')
		$(form).attr('name', 'question')
		$(form).attr('action', '/api/'+id+'/opinions/')
		var radioSection = document.createElement('section')
		for(var i =0; i < 5; i++){
			var rad = document.createElement('input')
			$(rad).attr('type', 'radio')
			$(rad).attr('name', 'opinion')
			$(rad).attr('value', i-2)
			if( i == 2 ){ $(rad).attr('checked',true) }
			var label = document.createElement('label')
			$(label).text(window.labels[i])
			$(label).append(rad)
			$(radioSection).append(label)
		}

		var buttonDiv = document.createElement('div')
		var otherOppinonButton = document.createElement('button')
		var showScaleButton = document.createElement('button')
		$(otherOppinonButton).attr('name','loadstats')
		$(otherOppinonButton).text('Other Opinions')
		$(buttonDiv).append(otherOppinonButton)
		$(showScaleButton).attr('name','showscale')
		$(showScaleButton).text('Voice yours')
		$(buttonDiv).append(showScaleButton)

		var successDiv = document.createElement('success')
		$(successDiv).attr('rel','success')
		$(successDiv).css('display','none')
		var thanksDiv = document.createElement('div')
		$(thanksDiv).addClass('thank-you')
		$(thanksDiv).css({'background-color' : 'black', 'text-align' : 'center'})
		$(thanksDiv).append( 
			$(document.createElement('h1')).text('Your vote has been recorded, thanks!')
			)
		$(successDiv).append(thanksDiv)
		$(form).append(radioSection)
		$(form).append(buttonDiv)
		$(form).append(successDiv)
		$(qWrapper).append(form)
		return qWrapper
	}
})

