from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk', 'username',
        )


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user= None

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('id or pw is wrong')
        self.user = user
        return data

    def to_representation(self, instance):
        token = Token.objects.get_or_create(user=self.user)[0]
        data = {
            'user': UserSerializer(self.user).data,
            'token': token.key,
        }
        return data