from django.conf import settings
from django.core.signing import TimestampSigner

def generate_phone_verify_token(phone_number: str) -> str:
    signer = TimestampSigner()
    token = signer.sign(phone_number)
    return token
