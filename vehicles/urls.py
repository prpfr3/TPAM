from django.urls import include, path, re_path
from . import views
app_name = 'vehicles'

urlpatterns = [

    re_path(r'^$', views.index, name='index'),
    path('most_popular_makes/', views.MostPopularMakesListView.as_view(), name='most_popular_makes'),
    re_path(r'^licensed_vehicles_list/$', views.UKLicensedVehiclesQuery, name='licensed_vehicles_list'),
    re_path(r'^most_popular_models_list/$', views.most_popular_models_list, name='most_popular_models_list'),
    ]
