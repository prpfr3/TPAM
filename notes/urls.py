from django.urls import path, reverse_lazy

from . import views

app_name = "notes"

urlpatterns = [
    path("", views.index, name="index"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/", views.post_list, name="post_list"),
    path("<int:post_id>/share/", views.post_share, name="post_share"),
    path("references/", views.references, name="references"),
    path("reference/<int:reference_id>/", views.reference, name="reference"),
    path("timeline", views.timeline, name="timeline"),
]
