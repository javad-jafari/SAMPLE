from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from otp.serializers import SendOTPSerializers, VerifyOTPSerializers
from rest_framework import status
from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from user.models import User
from user.task import login_token_agent_task


class SendOTPAPI(APIView):

    def post(self, request, format=None):

        serializer = SendOTPSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPAPI(KnoxLoginView):
    
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifyOTPSerializers

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):

            if serializer.save():

                user = get_object_or_404(
                    User, 
                    phone=serializer.validated_data["phone"]
                    )

                login(request, user)
                
                knox_token = super(VerifyOTPAPI, self).post(request,format=None)

                login_token_agent_task.delay(
                    user_id=request.user.id, 
                    digest=knox_token.data.get("digest"), 
                    agent=request.META['HTTP_USER_AGENT'].split()[1]
                    )
                    
                return knox_token
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)