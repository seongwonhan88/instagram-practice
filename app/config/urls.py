from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from config import views, settings
from posts import apis as post_apis
from members import apis as members_apis
from posts.views import tag_post_list

app_name = "config"



## app name tuple
urlpatterns_api_posts = ([
    path('posts/', post_apis.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', post_apis.PostDetail.as_view(), name='post-detail'),
    path('posts/<int:post_pk>/like/', post_apis.PostLikeCreateDestroy.as_view(), name='post-like'),
    path('posts/<int:post_pk>/unlike/', post_apis.PostLikeCreateDestroy.as_view(), name='post-unlike'),
    path('postlike/', post_apis.PostLikeCreateAPIView.as_view()),
    path('postlike/<int:pk>/', post_apis.PostLikeDestroyAPIView.as_view()),
], 'posts')


urlpatterns_api_members = ([
    path('auth-token/', members_apis.AuthTokenView.as_view()),
    path('user/<int:pk>/', members_apis.UserDetail.as_view()),
    path('user/profile/', members_apis.UserDetail.as_view()),
    path('view/<int:pk>/', members_apis.UserDetailAPIView.as_view()),
    path('view/profile/', members_apis.UserDetailAPIView.as_view()),
], 'members')


urlpatterns_api = ([
    path('posts/', include(urlpatterns_api_posts)),
    path('members/', include((urlpatterns_api_members)))
], 'api')



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('posts/', include('posts.urls')),
    path('members/', include('members.urls')),
    path('', views.index, name='index'),
    # path('', RedirectView.as_view(pattern_name='posts:post-list', name='index')),
    path('explore/tags/<tag_name>/', tag_post_list, name='tag-post-list'),
    # path('api/posts/', apis.PostList.as_view()),
    # path('api/posts/<int:pk>/', apis.PostDetail.as_view()),
    path('api/', include(urlpatterns_api))
]

# MEDIA_URL로 시작하는 URL은 statci()내의 serve()함수를 통해 처리
urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns