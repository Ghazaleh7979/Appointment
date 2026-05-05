from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from django.conf import settings

PHONE_VERIFY_SALT = "phone-verify-salt"

def get_phone_token_serializer():
    return URLSafeTimedSerializer(
        secret_key=settings.SECRET_KEY,
        salt=PHONE_VERIFY_SALT
    )
    
from django.core import signing
from django.conf import settings
from datetime import timedelta


class TimedTokenService:

    DEFAULT_EXPIRATION = 900  

    @staticmethod
    def generate(payload: dict, expires_in: int | None = None) -> str:
        expiration = expires_in or TimedTokenService.DEFAULT_EXPIRATION

        token = signing.dumps(
            payload,
            key=settings.SECRET_KEY,
            salt="secure-token",
        )

        return token

    @staticmethod
    def verify(token: str, max_age: int | None = None) -> dict:
        expiration = max_age or TimedTokenService.DEFAULT_EXPIRATION

        try:
            data = signing.loads(
                token,
                key=settings.SECRET_KEY,
                salt="secure-token",
                max_age=expiration,
            )
            return data

        except signing.SignatureExpired:
            raise ValueError("Token expired")

        except signing.BadSignature:
            raise ValueError("Invalid token")

