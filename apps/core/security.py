from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from django.conf import settings

PHONE_VERIFY_SALT = "phone-verify-salt"

def get_phone_token_serializer():
    return URLSafeTimedSerializer(
        secret_key=settings.SECRET_KEY,
        salt=PHONE_VERIFY_SALT
    )
