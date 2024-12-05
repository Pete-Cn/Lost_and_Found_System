function check() {
    var username = document.forms["myform"]["username"].value;
    var password1 = document.forms["myform"]["pwd1"].value;
    var password2 = document.forms["myform"]["pwd2"].value;
    var email = document.forms["myform"]["email"].value;
    if (username == null || username == "" ) {
        alert("用户名不能为空");
        return false;
    }
    if (email == null || email == "") {
        alert("邮箱不能为空");
        return false;
    }
    if (password1 == null || password1 == "" || password2 == null || password2 == "") {
        alert("密码不能为空");
        return false;
    }
    if (password1 != password2) {
        alert("两次密码不一致");
        return false;
    }
    var last = email.match("@mail.ustc.edu.cn");
    if (last == null || last == "") {
        alert("必须用科大邮箱注册");
        return false;
    }
}