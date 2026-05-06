import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_login_api_returns_access_and_sets_refresh_cookie():
    client = APIClient()

    User.objects.create_user(
        phone_number="09120000000",
        password="strongpass123",
        role="user",
        is_active=True,
        phone_verified=True,
    )

    response = client.post(
        "/api/users/login/",
        {
            "phone_number": "09120000000",
            "password": "strongpass123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" not in response.data

    assert "refresh_token" in response.cookies
    assert response.cookies["refresh_token"].value != ""



@pytest.mark.django_db
def test_login_api_invalid_password():
    client = APIClient()

    User.objects.create_user(
        phone_number="09120000000",
        password="strongpass123",
        role="user",
    )

    response = client.post(
        "/api/users/login/",
        {
            "phone_number": "09120000000",
            "password": "wrong-password",
        },
        format="json",
    )

    assert response.status_code == 400
