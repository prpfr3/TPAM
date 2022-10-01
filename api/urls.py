from django.urls import include, path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    re_path(r'^register/$', views.register),
    re_path(r'^login/$', views.login),
    # re_path(r'^builders/$', views.Builders.as_view(), name='builders'),
    re_path(r'^builders/$', views.builders, name='builders'),
    path('builder/<int:pk>', views.builder, name='builder'),
    re_path(r'^persons/$', views.persons, name='persons'),
    ]

# To investigate:- Appears in https://www.django-rest-framework.org/tutorial/3-class-based-views/
# urlpatterns = format_suffix_patterns(urlpatterns)