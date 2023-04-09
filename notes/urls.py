from django.urls import path, reverse_lazy

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.index, name='index'),

    path('topics/', views.TopicListView.as_view(), name='topics'), 
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topic/create/', views.TopicCreateView.as_view(success_url=reverse_lazy('notes:topics')), name='topic_create'),
    path('topic/<int:pk>/update/',views.TopicUpdateView.as_view(success_url=reverse_lazy('notes:topics')), name='topic_update'),
    path('topic/<int:pk>/delete', views.TopicDeleteView.as_view(success_url=reverse_lazy('notes:topics')), name='topic_delete'),

    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/create', views.PostCreateView.as_view(success_url=reverse_lazy('notes:topics')), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(success_url=reverse_lazy('notes:topics')), name='post_update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(success_url=reverse_lazy('notes:topics')), name='post_delete'),

    path('<int:post_id>/share/', views.post_share, name='post_share'),

    path('enamel_signs/', views.enamel_signs, name='enamel_signs'),
]