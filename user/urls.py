from django.urls import path
from user.views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    CurrentUserView, ChangeUserPasswordAPIView,
)

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("change-password/", ChangeUserPasswordAPIView.as_view(), name="change-password"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
]

app_name = "user"
