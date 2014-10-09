jQuery(document).ready(function($) {
	showMap($)
});

function showMap($){
	//dummy data for how it will be
	var data = {
		"states" : [
			{'majority': 'Inconclusive', 'state': 'US-WA', 'totals': [
				{'votes': 1, 'name': 'Strongly Disagree'}, 
				{'votes': 1, 'name': 'Disagree'}, 
				{'votes': 1, 'name': 'Neutral'}, 
				{'votes': 1, 'name': 'Agree'}, 
				{'votes': 1, 'name': 'Strongly Agree'}
				]
			}, 
			{'majority': 'Inconclusive', 'state': 'US-TX', 'totals': [
				{'votes': 1, 'name': 'Strongly Disagree'}, 
				{'votes': 1, 'name': 'Disagree'}, 
				{'votes': 1, 'name': 'Neutral'}, 
				{'votes': 1, 'name': 'Agree'}, 
				{'votes': 1, 'name': 'Strongly Agree'}
				]
			}, 
			{'majority': 'Inconclusive', 'state': 'US-MA', 'totals': [
				{'votes': 1, 'name': 'Strongly Disagree'}, 
				{'votes': 1, 'name': 'Disagree'}, 
				{'votes': 1, 'name': 'Neutral'}, 
				{'votes': 1, 'name': 'Agree'}, 
				{'votes': 1, 'name': 'Strongly Agree'}
				]
			}, 
			{'majority': 'Strongly Disagree', 'state': 'US-CA', 'totals': [
				{'votes': 2, 'name': 'Strongly Disagree'}, 
				{'votes': 1, 'name': 'Disagree'}, 
				{'votes': 1, 'name': 'Neutral'}, 
				{'votes': 1, 'name': 'Agree'}, 
				{'votes': 1, 'name': 'Strongly Agree'}
				]
			}, 
			{'majority': 'Inconclusive', 'state': 'US-GA', 'totals': [
				{'votes': 1, 'name': 'Strongly Disagree'}, 
				{'votes': 1, 'name': 'Disagree'}, 
				{'votes': 1, 'name': 'Neutral'}, 
				{'votes': 1, 'name': 'Agree'}, 
				{'votes': 1, 'name': 'Strongly Agree'}
				]
			}, 
			{'majority': 'Neutral', 'state': 'US-NH', 'totals': [
				{'votes': 1, 'name': 'Strongly Disagree'}, 
				{'votes': 1, 'name': 'Disagree'}, 
				{'votes': 2, 'name': 'Neutral'}, 
				{'votes': 1, 'name': 'Agree'}, 
				{'votes': 1, 'name': 'Strongly Agree'}
				]
			}, 
			{'majority': 'Inconclusive', 'state': 'US-VT', 'totals': [
				{'votes': 1, 'name': 'Strongly Disagree'}, 
				{'votes': 1, 'name': 'Disagree'}, 
				{'votes': 1, 'name': 'Neutral'}, 
				{'votes': 1, 'name': 'Agree'}, 
				{'votes': 1, 'name': 'Strongly Agree'}
				]
			}, 
			{'majority': 'Strongly Agree', 'state': 'US-NC', 'totals': [
				{'votes': 1, 'name': 'Strongly Disagree'}, 
				{'votes': 1, 'name': 'Disagree'}, 
				{'votes': 2, 'name': 'Neutral'}, 
				{'votes': 1, 'name': 'Agree'}, 
				{'votes': 7, 'name': 'Strongly Agree'}
				]
			}
		],
		"totals" : [
			{"votes" : 2, "name" : "Strongly Agree",	"state" : "US-AK"},
			{"votes" : 1, "name" : "Agree",				"state" : "US-VT"},
			{"votes" : 4, "name" : "Neutral",			"state" : "US-NH"},
			{"votes" : 1, "name" : "Disagree",			"state" : "US-CA"},
			{"votes" : 9, "name" : "Strongly Disagree", "state" : "US-TX"}
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
				return "vote-" + d.majority.replace(" ", "-")	
			})

			/* If we want to use the number of votes for each state to do something
			 * then we should do it here
			*/

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
		var votesXFunc = function(d) { return x(d.votes); }	

		/* Grab all groups and define how data will be transformed when entering */
		var bar = voteChart.selectAll("g").data(data.totals)
		var duration = 1000

    	bar.enter()
    		  .append("g")
      		  	.attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; })      	

      	/* For each bar we're going to add a rectangle ... */
      	bar.append("rect")
      	.attr("class", function(d){ return "vote vote-" + d.name.replace(" ","-") } )
      		.attr("height", barHeight - 1)
      		.attr("width", 0)
      		.transition().duration(duration).attr('width', votesXFunc)
      		.attr("width", votesXFunc)
      		
      		

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

