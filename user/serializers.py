from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
    
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields =["username", "phone","password","confirm_password"]

        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self,data):

        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Password confirme is incorrect")

        if len(data["password"]) < 5:
            raise serializers.ValidationError("password len must be bigger than 5")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        validated_data.pop('confirm_password',None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

