from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner

from apps.users.models import User


RESET_PASSWORD_SALT = "users.password.reset"
signer = TimestampSigner(salt=RESET_PASSWORD_SALT)


def request_password_reset_service(*, phone_number: str) -> User:

    user = User.objects.filter(phone_number=phone_number).first()

    if not user:
        return

    token = signer.sign(str(user.id))
    print(f"[DEBUG] Password reset token for user {user.phone_number}: {token}")
    return user


def generate_password_reset_token(*, user: User) -> str:
    return signer.sign(str(user.id))


def confirm_password_reset_service(*, token: str, new_password: str) -> User:
    try:
        user_id = signer.unsign(
            token,
            max_age=getattr(settings, "PASSWORD_RESET_TOKEN_MAX_AGE", 900)
        )
    except (BadSignature, SignatureExpired):
        raise ValidationError("Invalid or expired token.")

    user = User.objects.filter(id=user_id).first()
    if not user:
        raise ValidationError("Invalid or expired token.")

    user.set_password(new_password)
    user.save(update_fields=["password"])
    return user

