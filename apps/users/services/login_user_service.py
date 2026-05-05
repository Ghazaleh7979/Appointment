from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()    
    
DUMMY_PASSWORD_HASH = (
    "pbkdf2_sha256$390000$dummy$N2BzME1Ab1234567890abcdefghijklmn="
)

def login_user_service(*, phone_number: str, password: str) -> dict:

    try:
        user = User.objects.get(phone_number=phone_number)
    except User.DoesNotExist:
        check_password(password, DUMMY_PASSWORD_HASH)
        raise ValidationError("Invalid credentials")

    if not user.check_password(password):
        raise ValidationError("Invalid credentials") 

    if not user.is_active:
        raise ValidationError("Invalid credentials") 

    if not user.phone_verified:
        raise ValidationError("Invalid credentials") 

    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }
