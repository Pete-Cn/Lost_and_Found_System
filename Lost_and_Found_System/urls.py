"""
URL configuration for Lost_and_Found_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('login/', views.login_page, name="login"),
    path('signup/', views.signup_page, name="signup"),
    path('active/', views.active, name="active"),
    path('logout/', views.logout_page, name="logout"),
    path('item/', include("item.urls")),
    path('profile/<int:user_id>', views.profile, name="profile"),
    path('repwd/', views.repwd, name="repwd"),
    path('reset/', views.reset_pwd, name="reset"),
    path('setpwd/', views.set_pwd, name="setpwd")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)