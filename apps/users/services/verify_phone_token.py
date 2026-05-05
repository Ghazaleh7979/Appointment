from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.exceptions import ValidationError
from apps.users.models import User

PHONE_VERIFY_TOKEN_MAX_AGE = 300  # 5 minutes

def verify_phone_token(token: str) -> User:
    signer = TimestampSigner()

    try:
        phone_number = signer.unsign(
            token,
            max_age=PHONE_VERIFY_TOKEN_MAX_AGE
        )
    except SignatureExpired:
        raise ValidationError("Invalid or expired token")
    except BadSignature:
        raise ValidationError("Invalid or expired token")

    user = User.objects.filter(phone_number=phone_number).first()
    if not user:
        raise ValidationError("Invalid credentials")

    user.phone_verified = True
    user.save(update_fields=["phone_verified"])

    return user
