jQuery(document).ready(function($) {
	showMap($)
});

function showMap($){
	$('#map').usmap({
		stateSpecificStyles: window.dummyMapInfo,
		stateHoverStyles: {fill: 'white'},
		showLabels: true
	});
	/* This would be loaded via ajax */
	var stateMapping = {
		"vote-Strongly-Disagree" : ['MD'],
		"vote-Disagree" : ["VA"],
		"vote-Neutral" : ["GA"],
		"vote-Agree" : ["MO"],
		"vote-Strongly-Agree" : ["CA"]
	}

	function triggerState(classes,mapevent){
		var datum = stateMapping
		for( idx in classes){
			if( classes[idx] in datum ){
				var k =classes[idx]
				for (var i = datum[k].length - 1; i >= 0; i--) {
					var state = datum[k][i]
					$('#map').usmap('trigger', state, mapevent, null)         
				};
			}
		}
	}
	/* Bind events to the map in order to trigger flashing or highlighting the
	 * states that should be highlighted by the statistic
	 */
	$('#statistics').on("mouseover",'.vote',function(){

		var classes = $(this).attr('class').split(" ") 
		triggerState(classes, "mouseover")      
	})
	$('#statistics').on("mouseout",'.vote',function(){
		var classes = $(this).attr('class').split(" ") 
		triggerState(classes, "mouseout")      
	})

	/* Load up the data for the pie chart */
	var data = []
	for (var i = window.labelColors.length - 1; i >= 0; i--) {
		var clr = window.labelColors[i]
		var label = window.labels[i]
		var value = 1 //dummy val for now
		data.push({value: value, color: clr, label: label})
	};
	

	//dummy data for how it will be
	var data = [
		{"votes" : 2, "name" : "Strongly Agree"},
		{"votes" : 1, "name" : "Agree"},
		{"votes" : 4, "name" : "Neutral"},
		{"votes" : 1, "name" : "Disagree"},
		{"votes" : 3, "name" : "Strongly Disagree"}
	]

	/*
		The recommended indentation pattern for method chaining is four 
		spaces for methods that preserve the current selection and two 
		spaces for methods that change the selection.
	*/
	var width = 400
	var barHeight = 40; 
	var voteChart = d3.select("#svg_chart")
		.attr('width',width)

	var x = d3.scale.linear()
    	.range([0, width]);

	//d3.json("/api/call/for/data.json", function(error, data) {
		x.domain([ 
			0, 
			d3.max(data, function(d) { return d.votes; })
		])
		voteChart.attr("height", barHeight * data.length)

		/* Grab all groups and define how data will be transformed when entering */
		var bar = voteChart.selectAll("g")
      		  .data(data)
    		.enter()
    		  .append("g")
      		  	.attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; })

      	/* For each bar we're going to add a rectangle ... */
      	bar.append("rect")
      		.attr("width", function(d) { return x(d.votes); })
      		.attr("height", barHeight - 1)
      		.attr("class", function(d){ return "vote vote-" + d.name.replace(" ","-") } )

      	/* and we'll label it with it's # of votes */
      	bar.append("text")
      		.attr("x", function(d) { return 0; })
      		.attr("y", barHeight / 2)
      		.attr("dy", ".35em")
      		.attr("class", function(d){ return "vote vote-" + d.name.replace(" ","-") } )
      		.text(function(d) { 
      			return d.votes + (d.votes == 1 ? "person" : "people") + " " + d.name;
      		});



	//}

}

