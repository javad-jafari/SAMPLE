from rest_framework import serializers
from user.models import User
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from  config import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ChangePasswordSerializer(serializers.ModelSerializer):

    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_password')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['new_password'])
        instance.save()
        
        return instance




class ForgetPasswordSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('otp', 'new_password', 'confirm_password')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs



    def update(self, instance, validated_data):

        send_code=validated_data["otp"]

        try :
            cached_code=cache.get("code{}".format(instance.id)).split()[0]
        except:
            raise serializers.ValidationError({"otp": "code is expired"})

        if int(cached_code)==int(send_code):

            instance.set_password(validated_data['new_password'])
            instance.save()
        
            return instance
        raise serializers.ValidationError({"otp": "code is incorrect"})
        