from django.urls import path

from .views import (
    RegisterUserView,
    VerifyOTPView,
    LoginView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    LogoutView,
)

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register view"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "reset-password/",
        PasswordResetRequestView.as_view(),
        name="request-password-reset",
    ),
    path(
        "reset-password-confirm/",
        PasswordResetConfirmView.as_view(),
        name="reset-password",
    ),
]
