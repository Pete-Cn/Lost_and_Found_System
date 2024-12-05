function check() {
    var old_pwd = document.forms["myform"]["old_pwd"].value;
    var pwd1 = document.forms["myform"]["password1"].value;
    var pwd2 = document.forms["myform"]["password2"].value;
    if (old_pwd == null || old_pwd == "" ) {
        alert("原密码不能为空");
        return false;
    }
    if (pwd1 == null || pwd1 == "" || pwd2 == null || pwd2 == "") {
        alert("密码不能为空");
        return false;
    }
    if (pwd1 != pwd2) {
        alert("两次密码不一致");
        return false;
    }
}