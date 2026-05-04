import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.mark.django_db
def test_refresh_api_returns_new_access_token():
    client = APIClient()

    user = User.objects.create_user(
        phone_number="09120000000",
        password="test-password-123",
        role="user",
    )

    refresh = RefreshToken.for_user(user)

    response = client.post(
        "/api/users/refresh/",
        {
            "refresh": str(refresh)
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_refresh_api_invalid_token():
    client = APIClient()

    response = client.post(
        "/api/users/refresh/",
        {
            "refresh": "invalid-token"
        },
        format="json",
    )

    assert response.status_code == 400
