import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.mark.django_db
class TestLogoutAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.url = reverse("logout")

    def _create_user_and_tokens(self):
        user = User.objects.create_user(
            phone_number="09123456789",  # فیلد اجباری مدل تو
            password="StrongPass123!",
        )
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        return user, access_token, refresh_token


    def test_logout_with_valid_refresh_token_returns_204_and_blacklists_token(self):
        user, access_token, refresh_token = self._create_user_and_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.post(
            self.url,
            data={"refresh": refresh_token},
            format="json",
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        from rest_framework_simplejwt.exceptions import TokenError

        from rest_framework_simplejwt.tokens import RefreshToken as RT

        with pytest.raises(TokenError):
            RT(refresh_token).verify()

    def test_logout_without_refresh_token_returns_400(self):
        user, access_token, _ = self._create_user_and_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.post(
            self.url,
            data={}, 
            format="json",
        )

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "refresh" in response.data or "detail" in response.data

    def test_logout_with_invalid_refresh_token_returns_400(self):
        user, access_token, _ = self._create_user_and_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.post(
            self.url,
            data={"refresh": "invalid-token-value"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "detail" in response.data

    def test_logout_requires_authentication(self):
        response = self.client.post(
            self.url,
            data={"refresh": "whatever"},
            format="json",
        )

        assert response.status_code in (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)
