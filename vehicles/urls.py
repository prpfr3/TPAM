from django.urls import include, path, re_path
from . import views
app_name = 'vehicles'

urlpatterns = [

    re_path(r'^$', views.index, name='index'),
    #re_path(r'^UK_licensed_vehicles/(?P<make>[^/]+)/$', views.UKLicensedVehiclesListView.as_view(), name='UK_licensed_vehicles'),
    path('UK_licensed_vehicles/<type>/<make>/<model>/<variant>/', views.UKLicensedVehiclesListView.as_view(), name='UK_licensed_vehicles'),
    re_path(r'^choose_vehicle/$', views.choose_vehicle, name='choose_vehicle'),
    ]
