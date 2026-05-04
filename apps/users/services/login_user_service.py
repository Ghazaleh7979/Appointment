from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def login_user_service(*, phone_number: str, password: str) -> dict:
    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        raise ValidationError("Invalid credentials")

    if not user.is_active:
        raise ValidationError("User account is inactive")

    if not user.check_password(password):
        raise ValidationError("Invalid credentials")

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
