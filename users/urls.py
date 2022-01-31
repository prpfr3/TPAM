from datetime import datetime
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from . import forms, views


app_name = 'users'
urlpatterns = [
  # path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
  re_path(r'^login/$',
         LoginView.as_view
         (
             template_name='mainmenu/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
  # path('logout/', views.logout_view, name='logout'),
  path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
  path('register/', views.register, name='register'),
  ]