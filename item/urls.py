from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "items"

urlpatterns = [
    path("", views.item, name="item"),
    path("detail/<int:item_id>/", views.detail, name="detail"),
    path("search/", views.search, name="search"),
#    path("search/c/<int:campus_id>/", views.item, name="item_c"),
    path("post/", views.post_page, name="post_page"),
    path("load/", views.loaddata, name="loaddata"),
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)