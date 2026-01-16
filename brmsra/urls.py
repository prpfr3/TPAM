from django.urls import path

from . import views

app_name = "brmsra"

urlpatterns = [
    path("brmplans/", views.brmplans, name="brmplans"),
    path("brmplan/<int:plan_id>/", views.brmplan, name="brmplan"),
]