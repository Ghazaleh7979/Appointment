from django.urls import path
from .views import RegisterView
from .views import LoginView
from .views import RefreshTokenView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshTokenView.as_view(), name="token_refresh"),
]

