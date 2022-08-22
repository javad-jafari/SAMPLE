from unittest import result
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from rest_framework import serializers
from user.models import User
from random import randint
from operator_send import SendMCI, SendIrancell
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
        cache.set(result,timeout=CACHE_TTL)

        operator_path=self.find_operator(validated_data["phone"])

        if operator_path==1:
            SendMCI.sms_sender()
        elif operator_path==2:
            SendIrancell.sms_sender()

        return user


    def find_operator(self,phone):
        mci = "(0|\+98)?([ ]|-|[()]){0,2}9[9|1|]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}"
        iran = "(0|\+98)?([ ]|-|[()]){0,2}9[3|0|]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}"

        if re.match(mci, phone):
            return 1
        elif re.match(iran, phone):
            return 2 