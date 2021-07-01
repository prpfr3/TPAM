from django.urls import path, re_path, reverse_lazy 
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'maps'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^tube_map/$', views.tube_map, name='tube_map'),
    re_path(r'^tube_map_chart/$', views.tube_map_chart, name='tube_map_chart'),
    re_path(r'^gantt_chart/$', views.gantt_chart, name='gantt_chart'),
    re_path(r'^shareprice_chart/$', views.shareprice_chart, name='shareprice_chart'),
    re_path(r'^choose_location/$', views.choose_location, name='choose_location'),

    path('topics/', views.TopicListView.as_view(), name='topics'), 
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topic/create/', views.TopicCreateView.as_view(success_url=reverse_lazy('maps:topics')), name='topic_create'),
    path('topic/<int:pk>/update/',views.TopicUpdateView.as_view(success_url=reverse_lazy('maps:topics')), name='topic_update'),
    path('topic/<int:pk>/delete', views.TopicDeleteView.as_view(success_url=reverse_lazy('maps:topics')), name='topic_delete'),

    path('post/<int:pk>/create', views.PostCreateView.as_view(success_url=reverse_lazy('maps:topics')), name='post_create'),
    #re_path(r'^post/(?P<post_id>\d+)/update', views.post_update_view,
    #    name='post_update'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(success_url=reverse_lazy('maps:topics')), name='post_update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(success_url=reverse_lazy('maps:topics')), name='post_delete'),

    path('<int:post_id>/share/', views.post_share, name='post_share'),

    re_path(r'^heritage_map/(?P<county_name>[^/]+)/$', views.HeritageMapView.as_view(), name='heritage_map'),
    re_path(r'^heritage_sites/$', views.HeritageSiteListView.as_view(), name='heritage_sites'),
    re_path(r'^nearby_listed_buildings/$', views.GdUkListedBuildingsListView.as_view(), name='nearby_listed_buildings'), 
    re_path(r'^visits/$', views.VisitListView.as_view(), name='visits'),

    re_path(r'^heritage_site/(?P<heritage_site_id>\d+)/$', views.heritage_site, name='heritage_site'),
    re_path(r'^visit/(?P<visit_id>\d+)/$', views.visit, name='visit'),
]