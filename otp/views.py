from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from otp.serializers import SendOTPSerializers, VerifyOTPSerializers
from rest_framework import status
from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView
from user.models import User
from knox.models import AuthToken
from otp.throttles import OtpRateThrottle


class SendOTPAPI(APIView):
    
    throttle_classes = [OtpRateThrottle]

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
                
                token = AuthToken.objects.create(
                    user, self.request.META['HTTP_USER_AGENT']
                    )
                    
                return Response({ "token": token[1] })
                
            return Response(status=status.HTTP_408_REQUEST_TIMEOUT)
        return Response(status=status.HTTP_400_BAD_REQUEST)