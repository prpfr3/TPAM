from django.urls import path
from . import views

app_name = "storymaps"

urlpatterns = [
    path("storymaps/", views.storymaps, name="storymaps"),
    path("timelines/", views.timelines, name="timelines"),
    path("carousels/", views.carousels, name="carousels"),
    path("storymap/<slug:slug>/", views.storymap, name="storymap"),
    path("timeline/<slug:slug>/", views.timeline, name="timeline"),
    path("carousel/<slug:slug>/", views.carousel, name="carousel"),
    path("proxy_tile/<int:z>/<int:x>/<int:y>/", views.proxy_tile, name="proxy_tile"),
]
