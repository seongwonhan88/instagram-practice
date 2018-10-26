from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('create/', views.post_create, name='post-create'),
    path('<int:post_pk>/comments/create/', views.comment_create, name='comment-create'),
    # path('explore/tags/<tag_name>/', views.tag_post_list, name='tag-post-list'),
    # path('explore/tags/<tag_name>/?', views.tag_post_list),
]