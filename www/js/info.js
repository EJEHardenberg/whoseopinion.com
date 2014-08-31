$(document).ready(function() {
    showMap()
});

function showMap(){
    jQuery('#map').usmap({
        stateSpecificStyles: window.dummyMapInfo,
        stateHoverStyles: {fill: 'white'},
        showLabels: true
    });
    /* This would be loaded via ajax */
    var stateMapping = {
        "vote-Outraged" : ['MD'],
        "vote-Disagree" : ["VA"],
        "vote-Neutral" : ["GA"],
        "vote-Agree" : ["MO"],
        "vote-Support" : ["CA"]
    }

    function triggerState(classes,mapevent){
        var datum = stateMapping
        for( idx in classes){
            if( classes[idx] in datum ){
                var k =classes[idx]
                for (var i = datum[k].length - 1; i >= 0; i--) {
                    var state = datum[k][i]
                    jQuery('#map').usmap('trigger', state, mapevent, null)         
                };
            }
        }
    }
    /* Bind events to the map in order to trigger flashing or highlighting the
     * states that should be highlighted by the statistic
     */
     jQuery('#statistics li.vote').on("mouseover",function(){
        var classes = this.className.split(" ") 
        triggerState(classes, "mouseover")      
     })
     jQuery('#statistics li.vote').on("mouseout",function(){
        var classes = this.className.split(" ") 
        triggerState(classes, "mouseout")      
     })
     
}

