jQuery( document ).ready(function( $ ) {
	console.info('tutorial.js loaded')
	/* Check for cookie that says not to show the tutorial */

	/* Display the first area to point to and click for the tutorial */

	/* Continue with adding events and states and things to teach the user */

	/* At any point they stop, remember their choice and do not bother them again */

	var show = false
	function showHideTip(tip){
		/* Uses global show var */
		if(show) tip.tooltipster('show')
		else tip.tooltipster('hide')
	}
	
	$('[name=vote-help]').tooltipster()
	$('[name=vote-help]').click(function(){ 
		show = !show 
		categoryHelp()
		otherOppHelp()
		voiceYours()
		var enableDisable = show ? 'enable' : 'disable'
		$('.tooltipstered:not([name=vote-help])').tooltipster(enableDisable )
		$(this).text( show ? 'Help Mode On' : '(?)')

	})

	function categoryHelp(){
		var tip = $('[name=category-header]')
		tip.tooltipster({
			content: 'Select a category below to display statements to vote on',
		})
		showHideTip(tip)
	}

	function otherOppHelp(){
		var tip = $('[name=loadstats]')
		tip.tooltipster({
			content: 'Show other user\'s votes, see how regions think, and view more information on the subject'
		})
		showHideTip($(tip[2]))
	}

	function voiceYours(){
		var tip = $('[name=showscale]')
		tip.tooltipster({
			content: 'Click to reveal the voting scale'
		})
		showHideTip($(tip[4]))
	}

	

})