from rest_framework.views import APIView
from rest_framework.response import Response
from otp.serializers import SendOTPSerializers
from rest_framework import status


class SendOTPAPI(APIView):

    def post(self, request, format=None):

        serializer = SendOTPSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):

            serializer.save()

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
