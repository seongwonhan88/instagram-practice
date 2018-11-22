from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializers import UserSerializer, AuthTokenSerializer

User = get_user_model()


class AuthTokenView(APIView):
    """
    takes usename and password, returns validation token and user info
    """
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        raise Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            user = get_object_or_404(User, pk=pk)
        else:
            user = request.user
            if not user.is_authenticated:
                raise NotAuthenticated()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        if lookup_url_kwarg not in self.kwargs:
            if not self.request.user.is_authenticated:
                raise NotAuthenticated()
            return self.request.user
        return super().get_object()
