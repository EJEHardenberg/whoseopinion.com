var ranks = ["red", "orange","blue","green","olive"]
$(document).ready(function() {
    $('#map').usmap({
    	stateSpecificStyles: window.dummyMapInfo,
  		stateHoverStyles: {fill: 'white'}
    });
});
