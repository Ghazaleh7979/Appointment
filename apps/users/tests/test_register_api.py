import pytest
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.mark.django_db
def test_register_api_creates_user():
    client = APIClient()

    payload = {
        "phone_number": "09120000001",
        "password": "strongpass123",
        "full_name": "Test User"
    }

    response = client.post("/api/users/register/", payload, format="json")

    assert response.status_code == 201
    assert User.objects.filter(phone_number="09120000001").exists()


@pytest.mark.django_db
def test_register_api_ignores_role_from_client():
    client = APIClient()

    payload = {
        "phone_number": "09120000002",
        "password": "strongpass123",
        "full_name": "Test User",
        "role": User.Role.ADMIN
    }

    response = client.post("/api/users/register/", payload, format="json")

    user = User.objects.get(phone_number="09120000002")

    assert response.status_code == 201
    assert user.role == User.Role.CUSTOMER

