from rest_framework import serializers
from django.contrib.auth import get_user_model
import re


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
        )

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def check_name(self, value):

        if not value.isalpha():
            raise serializers.ValidationError(
                "The name must contain only letters"
            )

        elif (
                not bool(re.fullmatch("[A-Za-z]+", value))
                or bool(re.fullmatch(r'[À-ÙÜÞßª²¯¥à-ùüþÿº³¿´]+', value))
        ):
            raise serializers.ValidationError(
                "The name must contain only English letters or Cyrillic"
            )

        elif len(value) < 2:
            raise serializers.ValidationError(
                "The length should be longer than 1"
            )

        elif len(value) > 31:
            raise serializers.ValidationError(
                "The length should be lower than 1"
            )

        elif value[1].islower():
            raise serializers.ValidationError(
                "The first letter of the name must be capitalized"
            )

    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")

        self.check_name(first_name)
        self.check_name(last_name)

        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "profile_picture")


class ChangeUserPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if value == self.initial_data.get("old_password"):
            raise serializers.ValidationError(
                "The new password cannot be the same as the previous password!"
            )

        if len(value) < 8:
            raise serializers.ValidationError(
                "The new password must be at least 8 characters long!"
            )

        if str(value).isalpha():
            raise serializers.ValidationError(
                "The new password cannot consist of only letters!"
            )

        if str(value).isdigit():
            raise serializers.ValidationError(
                "The new password cannot consist of only digits!"
            )

        return value
