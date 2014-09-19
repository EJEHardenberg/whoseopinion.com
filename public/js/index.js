jQuery( document ).ready(function( $ ) {
	console.info("Index.js loaded")	

	var loadQuestionsEvent = "load_questions"
	var popularCategoryFlag = -1

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
		console.log('displayQuestions')

	}

	function loadQuestions(e){
		console.log('loadQuestions', e.category)
		var categoryId = parseInt(e.category)
		if(isNaN(categoryId)){
			console.debug("Invalid category id being passed to function")
			return
		}
		var url = window.apiuri +  'category/' + categoryId + '/'
		$.getJSON(url, displayQuestions)
	}
	$('#category-list').on('click', 'a', function(evt){
		var id = $(this).attr('href').split(':')[1]
		$.event.trigger({
			type: loadQuestionsEvent,
			category: id
		})
	})

	$(document).on(loadQuestionsEvent, loadQuestions)
})