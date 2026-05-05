import pytest
from rest_framework.test import APIRequestFactory
from django.contrib.auth import get_user_model
from apps.users.api.permissions import IsAdminPermission

User = get_user_model()

@pytest.mark.django_db
def test_is_admin_permission_allows_admin():
    user = User.objects.create_user(phone_number="...", password="...", role=User.Role.ADMIN)
    factory = APIRequestFactory()
    request = factory.get("/")
    request.user = user
    perm = IsAdminPermission()
    assert perm.has_permission(request, None) is True

@pytest.mark.django_db
def test_is_admin_permission_denies_non_admin():
    user = User.objects.create_user(phone_number="...", password="...", role=User.Role.STAFF)
    factory = APIRequestFactory()
    request = factory.get("/")
    request.user = user
    perm = IsAdminPermission()
    assert perm.has_permission(request, None) is False
