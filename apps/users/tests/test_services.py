from django.test import TestCase

from apps.users.models import User
from apps.users.services.create_user_service import create_user_service


class CreateUserServiceTests(TestCase):
    def test_create_user_service_creates_user_with_correct_fields(self):
        user = create_user_service(
            phone_number="09120000000",
            full_name="حسین",
            password="test-password-123",
        )

        user_from_db = User.objects.get(id=user.id)

        self.assertEqual(user_from_db.phone_number, "09120000000")
        self.assertEqual(user_from_db.full_name, "حسین")
        self.assertTrue(user_from_db.is_active)
        self.assertEqual(user.role, "user")

        self.assertNotEqual(user_from_db.password, "test-password-123")
        self.assertTrue(user_from_db.check_password("test-password-123"))

    def test_create_user_service_requires_unique_phone_number(self):
        create_user_service(
            phone_number="09120000000",
            full_name="کاربر اول",
            password="pass1",
        )

        with self.assertRaises(Exception):
            create_user_service(
                phone_number="09120000000",
                full_name="کاربر دوم",
                password="pass2",
            )


from django.test import TestCase
from apps.users.models import User
from apps.users.services.change_password_service import change_password_service


class ChangePasswordServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09120000000",
            full_name="حسین",
            password="initial-password",
        )

    def test_change_password_service_updates_user_password(self):
        change_password_service(user=self.user, new_password="new-secure-password-123")

        self.assertFalse(self.user.check_password("initial-password")) 
        self.assertTrue(self.user.check_password("new-secure-password-123")) 

    def test_change_password_service_hashes_new_password(self):
        change_password_service(user=self.user, new_password="hashed-password")
        self.assertNotEqual(self.user.password, "hashed-password")  
        
        
from django.test import TestCase
from apps.users.models import User
from apps.users.services.activate_user_service import activate_user_service
from apps.users.services.deactivate_user_service import deactivate_user_service


class UserActivationServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="09121111111",
            full_name="Ali",
            password="test-password",
        )

    def test_deactivate_user_service_sets_is_active_false(self):
        deactivate_user_service(user=self.user)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activate_user_service_sets_is_active_true(self):
        # اول غیرفعالش کنیم
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        activate_user_service(user=self.user)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_deactivate_is_idempotent(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        deactivate_user_service(user=self.user)

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_activate_is_idempotent(self):
        activate_user_service(user=self.user)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

