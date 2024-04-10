from django.urls import path
from . import views

app_name = "storymaps"

urlpatterns = [
    path("storymaps/", views.storymaps, name="storymaps"),
    path("storymap/<slug:slug>/", views.storymap, name="storymap"),
]
