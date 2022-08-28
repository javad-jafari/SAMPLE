from django.shortcuts import get_object_or_404
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import serializers
from django.conf import settings
from django.core.cache import cache
from knox.models import AuthToken
from otp.tasks import send_otp_task
from user.models import User
from config.settings import IRANCELL_PATTERN, MCI_PATTERN
import re

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)




class SendOTPSerializers(serializers.Serializer):

    phone = serializers.CharField()


    def validate(self,data):

        try :
             User.objects.get(phone=data["phone"])
        
        except User.DoesNotExist:
            raise serializers.ValidationError("phone number didn't not Found")
        
        return data


    def create(self, validated_data):
        
        user = User.objects.get(phone=validated_data["phone"])
        operator_path=self.find_operator(validated_data["phone"])

        send_otp_task.delay(user.id, operator_path)

        return operator_path


    def find_operator(self,phone):

        if re.match(MCI_PATTERN, phone):
            return 1
        elif re.match(IRANCELL_PATTERN, phone):
            return 2 







class VerifyOTPSerializers(serializers.ModelSerializer):

    code = serializers.CharField()
    phone = serializers.CharField()

    class Meta:
        model = AuthToken
        fields = ('code', 'phone')

    def validate(self,data):

        if int(data["code"]) not in range(1000,9999):
            raise serializers.ValidationError({"otp":"code is invalid"})
        
        return data


    def create(self, validated_data):

        agent = self.context

        
        user = get_object_or_404(
            User, 
            phone=validated_data["phone"]
            )

        send_code=validated_data["code"]

        try :
            cached_code=cache.get("code{}".format(user.id)).split()[0]
        except:
            raise serializers.ValidationError({"otp": "code is expired"})

        if int(cached_code)==int(send_code):
            return 1
        raise serializers.ValidationError({"otp":"code is invalid"})
        
