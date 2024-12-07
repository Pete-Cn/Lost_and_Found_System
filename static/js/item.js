var campus_select = document.getElementById('campus_select');
var building_all = document.getElementsByClassName('building');
var selected_buildings = document.getElementsByClassName('selected_buildings');
var campus_chosen;

window.addEventListener('load', function(){

    var building_select = document.getElementById('building_select');
    for(var i = 0; i < building_select.length; i++) 
        building_select[i].selected = false;
    
    for(var i = 0; i < selected_buildings.length; i++) {
        var name = selected_buildings[i].innerText;
        console.log(name);
        for(var j = 0; j < building_select.length; j++) {
            if (building_select[j].innerHTML == name) {
                building_select[j].selected = true;
            } 
        }
    }
});
function changeTag(building_type) {
    campus_chosen = campus_select.value;
    for (var i = 0; i < building_all.length; i++) {
        building_all[i].style.display = "none";
        if (building_all[i].id.includes( campus_chosen + "*" ) || campus_chosen == "0") {
            if (building_all[i].id.includes("*" + building_type) || building_type == "0") 
                building_all[i].style.display = "block";
        } 
    }
}
