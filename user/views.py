from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import generics
from user.models import User,LoginToken
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
from user.task import login_token_agent_task




class RegisterAPI(generics.CreateAPIView):

    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer






class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        login(request, user)

        knox_token = super(LoginView, self).post(request,format=None)

        login_token_agent_task.delay(
            user_id=request.user.id,
            digest=knox_token.data.get("digest"),
            agent=request.META['HTTP_USER_AGENT'].split()[1]
            )
            
        return knox_token


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





class HelloAPI(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):

        return Response("hello world")
