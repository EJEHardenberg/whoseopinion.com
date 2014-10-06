jQuery(document).ready(function($) {
	showMap($)
});

function showMap($){
	//dummy data for how it will be
	var data = [
		{"votes" : 2, "name" : "Strongly Agree",	"state" : "US-AK"},
		{"votes" : 1, "name" : "Agree",				"state" : "US-VT"},
		{"votes" : 4, "name" : "Neutral",			"state" : "US-NH"},
		{"votes" : 1, "name" : "Disagree",			"state" : "US-CA"},
		{"votes" : 3, "name" : "Strongly Disagree", "state" : "US-TX"}
	]


	var chartContainer = d3.select("#map")
	d3.xml("/svgs/usa.svg", function(error, documentFragment){
		if (error) {console.error(error); return}

		var svgNode = documentFragment.getElementsByTagName("svg")[0];
		chartContainer.html("")
		chartContainer.node().appendChild(svgNode)

		var innerSVG = d3.select("svg");
		innerSVG.attr('height', chartContainer.attr('height'))

		var paths = innerSVG.selectAll("path")
		
		var joined = paths.data(data, function(d){ 
			/* Key function, mind the gaps */
			return (d && d.state) || d3.select(this).attr("id")
		})

		joined.attr("class", function(d){		
			if( typeof d == "undefined" ){
				return "land"
			}
			console.log("setting class",d)	
			return "vote-" + d.name.replace(" ", "-")	
		})

	})

	
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
      			return d.name + ": " + d.votes
      		});

	//}

}

