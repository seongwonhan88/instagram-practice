import json

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated, APIException
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
        serializer = PostLikeSerializer(data={**request.data,'post': post_pk}, context={'request':request})
        if serializer.is_valid():
            if PostLike.objects.filter(
                post=serializer.validated_data['post'],
                user=request.user
            ).exists():
                raise APIException('이미 좋아요 한 포스트 입니다')
            serializer.save()
            return Response(serializer, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
