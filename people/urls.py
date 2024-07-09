from django.urls import path
from . import views

app_name = "people"

urlpatterns = [
    path("", views.index, name="index"),
    path("people/", views.people, name="people"),
    path("person/<slug:slug>/", views.person, name="person"),
    path("people_storyline/", views.people_storyline, name="people_storyline"),
    path("people_vis_timeline/", views.people_vis_timeline, name="people_vis_timeline"),
]
