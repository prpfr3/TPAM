from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    # path('manufacturers/', views.Manufacturers.as_view(), name='manufacturers'),
    path('manufacturers/', views.manufacturers, name='manufacturers'),
    path('manufacturer/<int:pk>', views.manufacturer, name='manufacturer'),
    path('persons/', views.persons, name='persons'),
    ]

# To investigate:- Appears in https://www.django-rest-framework.org/tutorial/3-class-based-views/
# urlpatterns = format_suffix_patterns(urlpatterns)