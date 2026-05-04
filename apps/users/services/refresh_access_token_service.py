from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError


def refresh_access_token_service(*, refresh_token: str) -> dict:
    try:
        refresh = RefreshToken(refresh_token)
    except Exception:
        raise ValidationError("Invalid refresh token")

    return {
        "access": str(refresh.access_token)
    }
