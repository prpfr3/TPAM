from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    # path('builders/', views.Builders.as_view(), name='builders'),
    path('builders/', views.builders, name='builders'),
    path('builder/<int:pk>', views.builder, name='builder'),
    path('persons/', views.persons, name='persons'),
    ]

# To investigate:- Appears in https://www.django-rest-framework.org/tutorial/3-class-based-views/
# urlpatterns = format_suffix_patterns(urlpatterns)