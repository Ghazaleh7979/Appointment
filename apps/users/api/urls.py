from django.urls import path
from .views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetRequestView, RefreshTokenView, RegisterView, VerifyPhoneView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
    path("auth/verify-phone/", VerifyPhoneView.as_view()),
    path("password-reset/request/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("logout/", LogoutView.as_view(), name="logout"),
]

