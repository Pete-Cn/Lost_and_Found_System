var campus_select = document.getElementById("campus_select");
var building_all = document.getElementsByClassName("building");
var campus_chosen;

document.readyState(function(){
    ('')
})

function changetag(building_type) {
    campus_chosen = campus_select.value;
    for (var i = 0; i < building_all.length; i++) {
        building_all[i].style.display = "none";
        if (building_all[i].id.includes( campus_chosen + "*" ) || campus_chosen == "0") {
            if (building_all[i].id.includes("*" + building_type) || building_type == "0") 
                building_all[i].style.display = "block";
        } 
    }
}