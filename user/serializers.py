from rest_framework import serializers
from django.contrib.auth import get_user_model


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
