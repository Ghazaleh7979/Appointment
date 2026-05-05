import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_login_api_returns_tokens():
    client = APIClient()

    user = User.objects.create_user(
        phone_number="09120000000",
        password="strongpass123",
        role="user",
        is_active=True,        # ✅ اضافه کن
        phone_verified=True,   # ✅ اضافه کن
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
    assert "refresh" in response.data



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
