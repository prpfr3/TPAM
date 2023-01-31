from django.urls import path
from . import views
app_name = 'vehicles'

urlpatterns = [

    path('', views.index, name='index'),
    path('licensed_vehicles_list/', views.UKLicensedVehiclesQuery, name='licensed_vehicles_list'),
    path('most_popular_makes/', views.MostPopularMakesListView.as_view(), name='most_popular_makes'),
    path('most_popular_models_list/', views.most_popular_models_list, name='most_popular_models_list'),
    ]
