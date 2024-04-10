from django.urls import path
from . import views

app_name = "timelines"

urlpatterns = [
    path("timelines/", views.timelines, name="timelines"),
    path("timeline/<slug:slug>/", views.timeline, name="timeline"),
]
