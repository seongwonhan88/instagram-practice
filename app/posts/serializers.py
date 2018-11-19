from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Post, Comment, PostLike

User = get_user_model()


class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.SlugRelatedField(many=True, read_only=True, slug_field='content')
    like_users = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('pk', 'author', 'photo', 'created_at', 'modified_at', 'like_users', 'comments',)

        read_only_fields = (
            'author',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')


class CommentSerializer(serializers.Serializer):
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = ('author', 'post', 'content')


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = PostLike
        fields = ('user', 'post', 'created_at')
        read_only_fields = ('user',)
