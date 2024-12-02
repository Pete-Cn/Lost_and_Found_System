from django.shortcuts import render, render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .forms import SignUpForm, User 
from django.contrib.auth.decorators import login_required
from . import settings

import uuid, time
import datetime

def index(request):
    print(request.user.username)
    return render(request, "index.html")

def split_after(a, b):
    parts = a.split(b, 1)
    if len(parts) > 1:
        return parts[1]
    else:
        return ''

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = split_after(request.get_full_path(), "/?next=")
        print(username)
        print(password)
        if username and password:
            user = authenticate(username=username, password=password)
            print(type(user))
            if user is not None and user.is_active == True:
                login(request, user)
                if  next != "":
                    return redirect(next)
                else:
                    return redirect(reverse('index'))
            else:
                return render(request, 'login.html', {"error_message": "用户名或密码错误"})
        else:
            return render(request, 'login.html', {"error_message": "请输入用户名或密码"})
    
    return render(request, 'login.html')

def signup_page(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        form.is_valid()
        username = form.cleaned_data["username"]
        password = form.cleaned_data['password1']

        if username == None:
            username = request.POST.get('username')
            user = User.objects.get(username=username)
            if  user.is_active == False:

                requested_time = request.session.get('requested_time')
                current_time = time.mktime(datetime.datetime.now().timetuple())

                if requested_time is None:
                    request.session['requested_time'] = current_time
                    print(123)
                else:
                    time_difference = current_time - requested_time
                    print(time_difference)
                    if  time_difference > 200:
                        user.set_password(password)
                        user.save()
                    else:
                        return render(request, 'signup.html', {'form': form, 'error_message': "操作过于频繁"})     
            else:
                return render(request, 'signup.html', {'form': form, 'error_message': "邮箱已被注册"})
        else:
            user = User.objects.create_user(username=username, password=password, is_active=False)
        
        token = str(uuid.uuid4()).replace('-','')
        request.session[str(token)] = str(user.id)
        request.session.save()
        path = "127.0.0.1:8000" + reverse('active') + "?token=" + token
        msg = f"""
        <!DOCTYPE html>
        <html>
        <body>
            <p>请点击<a href="{path}" style="text-decoration:none;">此链接</a>激活<p>
            <br>
            <p>或直接访问以下链接<p>
            <p>{path}<p>
        </body>
        </html>
        """

        print(user.email)
        send_mail(subject="【验证链接】用于激活您的账号", from_email=settings.EMAIL_FROM, recipient_list=[user.username,], message="",  html_message=msg,)
        return render(request, 'index.html', {'error_message': "邮件已发送，请访问邮件链接激活账户"})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

def active(request):
    token = request.GET.get('token')
    uid = request.session.get(token)
    user = User.objects.get(id=uid)
    user.is_active = True
    user.save()
    return render(request, 'login.html', {'error_message': "账户已成功激活"})

@login_required
def logout_page(request):
    logout(request)
    return render(request, "index.html", {"error_message": "您已成功登出"})    

@login_required
def profile(request, user_id):
    if request.user.id == user_id:
        return render(request, "profile.html",)
    else:
        return HttpResponse("您无权查看此页面")
    
def repwd(request):
    if request.method == "POST":
        username=request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            if user.is_active == True:
                token = str(uuid.uuid4()).replace('-','')
                request.session[str(token)] = str(user.id)
                request.session.save()
                path = "127.0.0.1:8000" + reverse('reset') + "?token=" + token
                msg = f"""
                <!DOCTYPE html>
                <html>
                <body>
                    <p>请点击<a href="{path}" style="text-decoration:none;">此链接</a>重置密码<p>
                    <br>
                    <p>或直接访问以下链接<p>
                    <p>{path}<p>
                </body>
                </html>
                """
                send_mail(subject="【验证链接】用于重置您账号的密码", from_email=settings.EMAIL_FROM, recipient_list=[user.username,], message="",  html_message=msg,)
                return render(request, 'index.html', {'error_message': "邮件已发送，请访问邮件链接激活账户"})
            else:
                return render(request, 'repwd.html', {"error_message": "账户未激活"})
        except:
            return render(request, 'repwd.html', {"error_message": "邮箱未注册"})
    return render(request, 'repwd.html')

def reset_pwd(request):
    token = request.GET.get('token')
    uid = request.session.get(token)
    user = User.objects.get(id=uid)
    user.set_password("12345678")
    user.save()
    return render(request, 'login.html', {'error_message': "密码已被重置为12345678"})

@login_required
def set_pwd(request):
    if request.method == "POST":
        new_pwd = request.POST.get('pwd1')
        try:
            user = User.objects.get(id=request.user.id)
            user.set_password(new_pwd)
            print(new_pwd)
            user.save()
            return redirect(reverse('logout'))
        except:
            return render(request, "set_pwd.html", {"error_message": "密码修改失败"})
    return render(request, "set_pwd.html")