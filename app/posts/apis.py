import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
from .serializers import PostListSerializer, UserSerializer, CommentSerializer, PostLikeSerializer
from .models import HashTag, Post, Comment, PostLike

User = get_user_model()

class PostList(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)

#
# class CommentList(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

class PostLikeCreate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, post_pk):
        user = request.user
        post = get_object_or_404(Post, pk=post_pk)
        if PostLike.objects.filter(user=user, post=post).exists():
            data = {
                'detail': '이미 좋아요를 누른 포스트입니다'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        post_like = PostLike.objects.create(user=user, post=post)
        return Response(status=status.HTTP_201_CREATED)

class PostLikeDelete(APIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)



def tag_search(request):
    #URL: /posts/api/tag-search/
    # request.GET
    # search_keyword contains
    # "hashtag" items
    # dict list to httpresponse return


    keyword = request.GET.get('keyword')
    results = []
    if keyword:
        results = list(HashTag.objects.filter(name__istartswith=keyword).values())
        results=json.dumps(results)
    return HttpResponse(results, content_type='application/json')
