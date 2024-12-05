from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path("report/", views.report_page, name="report_page"),
]