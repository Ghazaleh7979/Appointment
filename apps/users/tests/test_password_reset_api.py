import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.services.password_reset import generate_password_reset_token

User = get_user_model()


@pytest.mark.django_db
class TestPasswordResetAPI:
    def setup_method(self):
        self.client = APIClient()
        self.request_url = "/api/users/password-reset/request/"
        self.confirm_url = "/api/users/password-reset/confirm/"

    def test_password_reset_request_returns_generic_message_for_existing_user(self):
        User.objects.create_user(
            phone_number="09120000001",
            password="OldPassword123",
        )

        response = self.client.post(
            self.request_url,
            {"phone_number": "09120000001"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "If this account exists, a reset token has been generated."

    def test_password_reset_request_returns_generic_message_for_non_existing_user(self):
        response = self.client.post(
            self.request_url,
            {"phone_number": "09129999999"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "If this account exists, a reset token has been generated."

    def test_password_reset_confirm_resets_password_successfully(self):
        user = User.objects.create_user(
            phone_number="09120000002",
            password="OldPassword123",
        )

        token = generate_password_reset_token(user=user)

        response = self.client.post(
            self.confirm_url,
            {
                "token": token,
                "new_password": "NewPassword123",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "Password has been reset successfully."

        user.refresh_from_db()
        assert user.check_password("NewPassword123") is True

    def test_password_reset_confirm_with_invalid_token_fails(self):
        user = User.objects.create_user(
            phone_number="09120000000",
            password="oldpass123",  # ✅ رمز اولیه
            role="user",
            is_active=True,
            phone_verified=True,
        )

        response = self.client.post(
            self.confirm_url,
            {
                "token": "invalid-token",
                "new_password": "NewPassword123",  # این نباید اعمال بشه
           },
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid or expired token." in str(response.data)

        user.refresh_from_db()
        assert user.check_password("oldpass123") is True  # ✅ رمز قدیمی باید باقی بمونه
        assert user.check_password("NewPassword123") is False  # ✅ رمز جدید نباید ست شده باشه

