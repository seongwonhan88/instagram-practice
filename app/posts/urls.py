from django.urls import path

from . import views, apis


app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('create/', views.post_create, name='post-create'),
    path('<int:post_pk>/comments/create/', views.comment_create, name='comment-create'),
    path('tag-search/', views.tag_search, name='tag-search'),
    path('<post_pk>/like-toggle/', views.post_like_toggle, name='post-like-toggle'),
    path('api/tag-search/', apis.tag_search, name='api-tag-search'),
]