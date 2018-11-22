from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.serializers import UserSerializer
from .models import Post, Comment, PostLike

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('author', 'content')

class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    # comments = serializers.SlugRelatedField(many=True, read_only=True, slug_field='content')
    # like_users = serializers.StringRelatedField(many=True, read_only=True)
    comments = CommentSerializer(many=True)
    is_like = serializers.SerializerMethodField(method_name=None)
    class Meta:
        model = Post
        fields = ('pk', 'author', 'photo', 'created_at', 'modified_at', 'like_users', 'comments','is_like')

        read_only_fields = (
            'author',
        )
    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                postlike= obj.postlike_set.get(user=user)
            except PostLike.DoesNotExist:
                return


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')



class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = PostLike
        fields = ('pk','user', 'post', 'created_at')
        read_only_fields = ('user',)
