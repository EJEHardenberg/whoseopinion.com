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
     $('#statistics li.vote').on("mouseover",function(){
        var classes = this.className.split(" ") 
        triggerState(classes, "mouseover")      
     })
     $('#statistics li.vote').on("mouseout",function(){
        var classes = this.className.split(" ") 
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
     var ctx = document.getElementById("opinionChart").getContext("2d");
     var opinionChart = new Chart(ctx).Pie(data)
     
}

