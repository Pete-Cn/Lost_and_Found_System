function check() {
    var campus_found = document.forms["myform"]["campus_found"].value;
    var building_found = document.forms["myform"]["building_found"].value;
    var type = document.forms["myform"]["type"].value;
    var name = document.forms["myform"]["name"].value;
    if (campus_found == 0 || campus_found == null) {
        alert("请选择校区");
        return false;
    }
    if (name == "0" || name == null) {
        alert("名称不能为空");
        return false;
    }
    if (building_found == "0" || building_found == null) {
        alert("请选择建筑");
        return false;
    }
    if (type == "0" || type == null) {
        alert("请选择物品种类");
        return false;
    }
}

var imagebox = document.getElementById('imagebox');
var campus_select = document.getElementById('campus_select');
var building_all = document.getElementsByClassName('building')
function changetag(building_type) {
    campus_chosen = campus_select.value;
    for (var i = 0; i < building_all.length; i++) {
        building_all[i].style.display = "none";
        if (building_all[i].id.includes(campus_chosen + "*") || campus_chosen == "0") {
            if (building_all[i].id.includes("*" + building_type) || building_type == "0")
                building_all[i].style.display = "block";
        }
    }
}

function changebuilding() {
    var building = document.getElementById('building_box');
    var building_selected = document.getElementById('building_select');
    var str = [];
    for(var i = 0; i < building_selected.length; i++) {
        if (building_selected[i].selected) {
            str.push(building_selected[i].text);
        }
    }
    if (str.length > 1) {
        alert("只能选择一个建筑");
        for(var i = 0; i < building_selected.length; i++) {
            building_selected[i].selected = false;
        }
        return;
    } 
    building.innerHTML = str[0];
}

document.getElementById('imageInput').addEventListener('change', function () {
    var file = this.files[0];
    var reader = new FileReader();
    if (file) {
        reader.onload = function (e) {
            var img = document.getElementById('imagePreview');
            img.src = e.target.result;
            img.style.display = 'inline';
            imagebox.style.display = 'inline';
        };
        reader.readAsDataURL(file);
    }
});