from django.urls import path
from . import views

app_name = "locos"

urlpatterns = [
    path("", views.index, name="index"),
    path("loco_classes/", views.loco_classes, name="loco_classes"),
    path("loco_classes/<slug>/", views.loco_class, name="loco_class"),
    path("locomotives/", views.locomotives, name="locomotives"),
    path("locomotive/<int:locomotive_id>/", views.locomotive, name="locomotive"),
    path("photos/", views.photos, name="photos"),
    path("photo/<int:photo_id>/", views.photo, name="photo"),
]
