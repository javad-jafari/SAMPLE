from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from user.models import User
from rest_framework import permissions
from user.serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from knox.auth import TokenAuthentication
from django.contrib.auth import login,logout
from knox.models import AuthToken
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from knox.views import LogoutAllView as KnoxLogoutAllView





class RegisterAPI(generics.CreateAPIView):

    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user, self.request.META['HTTP_USER_AGENT'])
        return Response({ "token": token[1]})




class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']


        token = AuthToken.objects.create(user, self.request.META['HTTP_USER_AGENT'])
        return Response({ "token": token[1] })



class LogoutView(KnoxLogoutView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)
        return super(LogoutView, self).post(request, format=None)


class LogoutAllView(KnoxLogoutAllView):
    '''
    Log the user out of all sessions
    I.E. deletes all auth tokens for the user
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = ( permissions.IsAuthenticated,)

    def post(self, request, format=None):
        
        logout(request)
        return super(LogoutAllView, self).post(request, format=None)

