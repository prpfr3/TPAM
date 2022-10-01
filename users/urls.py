from datetime import datetime
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from . import forms, views


app_name = 'users'
urlpatterns = [
  re_path(r'^login/$',
         LoginView.as_view
         (
            template_name='users/login.html',
            authentication_form=forms.LoginForm,
            extra_context=
            {
                 'title': 'Log in',
                 'year' : datetime.now().year,
            }
         ),
         name='login'),
  path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
  path('register/', views.register, name='register'),
  ]