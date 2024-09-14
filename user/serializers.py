from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from user.models import User


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

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError(
                "The email can't be blank"
            )

        elif len(value) > 125:
            raise serializers.ValidationError(
                "Email must be less than 126 characters long"
            )

        elif User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "The user with this email address is already registered"
            )

        elif not ("@" in value):
            raise serializers.ValidationError(
                "The '@' symbol must be in email"
            )

        elif value.startswith("@"):
            raise serializers.ValidationError(
                "The email must contain the user's name"
            )

        elif len(value.split("@")) != 2:
            raise serializers.ValidationError(
                "Invalid email format"
            )

        user_name = value.split("@")[0]
        domain = value.split("@")[1]

        if not ("." in domain):
            raise serializers.ValidationError(
                "The email must contain the domain's name"
            )

        elif not bool(re.fullmatch("[a-z0-9]+", user_name)):
            raise serializers.ValidationError(
                "The username in the email must consist "
                "of English lowercase letters and numbers only"
            )

        domain_parts = domain.split(".")

        if len(domain_parts) < 2:
            raise serializers.ValidationError(

                "The domain must contain at least one dot"

            )

        for part in domain_parts:

            if not re.fullmatch("[a-z]+", part):
                raise serializers.ValidationError(

                    "The domain must consist of English lowercase letters only"

                )

        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError(
                "The password can't be blank"
            )

        elif len(value) < 6:
            raise serializers.ValidationError(
                "The length of password can't be less than 6 characters"
            )

        elif len(value) > 40:
            raise serializers.ValidationError(
                "The length of password must be less than 41 characters"
            )

        elif not any(char.isupper() for char in value):
            raise serializers.ValidationError(
                "The password must contain at least one capital letter"
            )

        elif not any(char in "!@#$%^&*-_" for char in value):
            raise serializers.ValidationError(
                "The password must contain at least one special character"
                " (!, @, #, $, %, ^, &, *, -, _)"
            )

        elif not any(char in "1234567890" for char in value):
            raise serializers.ValidationError(
                "The password must contain at least one number"
            )

        elif " " in value:
            raise serializers.ValidationError(
                "The password can't contain spaces"
            )

        elif "." in value:
            raise serializers.ValidationError(
                "The password can't contain dots"
            )

        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, value):

        if not value:
            raise serializers.ValidationError(
                "The email field can't be blank"
            )

        elif not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email does not exist"
            )

        return value

    def validate_password(self, value):

        if not value:
            raise serializers.ValidationError(
                "The password field can't be blank"
            )

        return value


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
