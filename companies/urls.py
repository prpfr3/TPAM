from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [

    path('', views.index, name='index'),

    path('companies/', views.companies, name='companies'),
    path('company/<int:company_id>/', views.company, name='company'),
    path('manufacturers/', views.manufacturers, name='manufacturers'),
    path('manufacturer/<int:manufacturer_id>/', views.manufacturer, name='manufacturer'),

    ]