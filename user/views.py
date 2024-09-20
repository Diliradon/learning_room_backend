from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .serializers import (
    RegisterUserSerializer,
    LoginSerializer,
    UserSerializer,
    ChangeUserPasswordSerializer,
)


class RegisterAPIView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny, )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = authenticate(username=request.data['email'], password=request.data['password'])
        if user is not None:
            login(request, user)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=serializer.data['email'], password=serializer.data['password'])
        if user is not None:
            login(request, user)
            return Response({"message": "Login is successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)


class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class ChangeUserPasswordAPIView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ChangeUserPasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            user = request.user

            if not user.check_password(old_password):
                return Response(
                    {"old_password": "Wrong password!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            new_password = serializer.data.get("new_password")

            user.set_password(new_password)
            user.save()
            return Response({"message": "Password is changed successfully"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def check_email(request):
    email = request.query_params.get("email")

    if not email:
        return Response({"message": "Email is required"}, status=400)

    user_exists = get_user_model().objects.filter(email=email).exists()

    if user_exists:
        return Response(
            {"message": "The user with the given email address is already registered in the system"}
        )

    return Response(
        {"message": "The user with the given email address is not yet registered in the system"}
    )