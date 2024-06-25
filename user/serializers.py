from rest_framework import serializers
from user.models import User
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "email")


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password")
        extra_kwargs = {"password": {"read_only": True}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("email", "password")
