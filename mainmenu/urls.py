from django.urls import path, re_path 
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'mainmenu'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)