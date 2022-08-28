from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from knox.models import AuthToken


class ListTokenSerializer(serializers.ModelSerializer):

    class Meta:

        model=AuthToken
        fields = ["agent", "digest"]
        