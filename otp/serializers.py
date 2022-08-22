from django.shortcuts import get_object_or_404
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from otp.operator import SendMCI, SendIrancell
from rest_framework import serializers
from django.conf import settings
from django.core.cache import cache
from user.models import User
from random import randint
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
        code = randint(1000,9999)
        result = "{} {}".format(code,user.id)
        cache.set("code{}".format(user.id) ,result,timeout=CACHE_TTL)

        operator_path=self.find_operator(validated_data["phone"])

        if operator_path==1:
            SendMCI().sms_sender()

        elif operator_path==2:
            SendIrancell().sms_sender()


        return operator_path


    def find_operator(self,phone):
        mci = "(0|\+98)?([ ]|-|[()]){0,2}9[9|1|]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}"
        iran = "(0|\+98)?([ ]|-|[()]){0,2}9[3|0|]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}"

        if re.match(mci, phone):
            return 1
        elif re.match(iran, phone):
            return 2 







class VerifyOTPSerializers(serializers.Serializer):

    code = serializers.CharField()
    phone = serializers.CharField()


    def validate(self,data):

        if int(data["code"]) not in range(1000,9999):
            raise serializers.ValidationError("code is invalid")
        
        return data


    def create(self, validated_data):
        
        user = get_object_or_404(
            User, 
            phone=validated_data["phone"]
            )

        send_code=validated_data["code"]
        cached_code=cache.get("code{}".format(user.id)).split()[0]

        if int(cached_code)==int(send_code):
            return 1
        return 0
