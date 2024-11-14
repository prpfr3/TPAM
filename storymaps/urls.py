from django.urls import path
from . import views

app_name = "storymaps"

urlpatterns = [
    path("storymaps/", views.storymaps, name="storymaps"),
    path("carousels/", views.carousels, name="carousels"),
    path("storymap/<slug:slug>/", views.storymap, name="storymap"),
    path("carousel/<slug:slug>/", views.carousel, name="carousel"),
    path("timelines/", views.timelines, name="timelines"),
    path("timeline/<slug:slug>/", views.timeline, name="timeline"),
]
