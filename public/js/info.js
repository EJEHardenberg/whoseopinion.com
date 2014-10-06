jQuery(document).ready(function($) {
	showMap($)
});

function showMap($){
	//dummy data for how it will be
	var data = {
		"totals" : [
			{"votes" : 2, "name" : "Strongly Agree",	},
			{"votes" : 1, "name" : "Agree",				},
			{"votes" : 4, "name" : "Neutral",			},
			{"votes" : 1, "name" : "Disagree",			},
			{"votes" : 3, "name" : "Strongly Disagree", }
		],
		"states" : [
			{"votes" : 2, "name" : "Strongly Agree",	"state" : "US-AK"},
			{"votes" : 1, "name" : "Agree",				"state" : "US-VT"},
			{"votes" : 4, "name" : "Neutral",			"state" : "US-NH"},
			{"votes" : 1, "name" : "Disagree",			"state" : "US-CA"},
			{"votes" : 3, "name" : "Strongly Disagree", "state" : "US-TX"}
		]
	}

	var id = window.location.hash.split(':')[1]
	console.debug("Loading",id)

	d3.json(window.apiuri +id+"/opinions/", function(error, data) {
		if (error) {console.error(error); return}
		console.info("Loaded Data", data)

		if(typeof data == "string"){
			data = JSON.parse(data)
		}

		var chartContainer = d3.select("#map")
		d3.xml("/svgs/usa.svg", function(error, documentFragment){
			if (error) {console.error(error); return}

			var svgNode = documentFragment.getElementsByTagName("svg")[0];
			chartContainer.html("")
			chartContainer.node().appendChild(svgNode)

			var innerSVG = d3.select("svg");
			innerSVG.attr('height', chartContainer.attr('height'))

			var paths = innerSVG.selectAll("path")
			
			var joined = paths.data(data.states, function(d){ 
				/* Key function, mind the gaps */
				return (d && d.state) || d3.select(this).attr("id")
			})

			joined.attr("class", function(d){		
				if( typeof d == "undefined" ){
					return "land"
				}
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
	    	.range([0, width])
			.domain([ 
				0, 
				d3.max(data.totals, function(d) { return d.votes; })
			])

		voteChart.attr("height", barHeight * data.totals.length)

		/* Grab all groups and define how data will be transformed when entering */
		var bar = voteChart.selectAll("g")
      		  .data(data.totals)
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

	})//end load json
}

