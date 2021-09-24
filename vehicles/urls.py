from django.urls import include, path, re_path
from . import views
app_name = 'vehicles'

urlpatterns = [

    re_path(r'^$', views.index, name='index'),
    path('UK_licensed_vehicles/<type>/<make>/<model>/<variant>/', views.UKLicensedVehiclesListView.as_view(), name='UK_licensed_vehicles'),
    path('most_popular_models/<type>/<year>/', views.MostPopularModelsListView.as_view(), name='most_popular_models'),
    path('most_popular_makes/', views.MostPopularMakesListView.as_view(), name='most_popular_makes'),
    re_path(r'^choose_vehicle/$', views.choose_vehicle, name='choose_vehicle'),
    re_path(r'^most_popular_models_selection/$', views.most_popular_models_selection, name='most_popular_models_selection'),
    ]
