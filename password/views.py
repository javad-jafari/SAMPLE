from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from user.models import User
from rest_framework.permissions import IsAuthenticated   
from knox.auth import TokenAuthentication
from password.serializers import ChangePasswordSerializer





class ChangePasswordView(generics.UpdateAPIView):

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

