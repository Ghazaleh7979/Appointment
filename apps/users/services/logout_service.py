from rest_framework_simplejwt.tokens import RefreshToken


def logout_service(*, refresh_token: str) -> None:
    token = RefreshToken(refresh_token)
    token.blacklist()