from django.test import TestCase
from apps.users.models import User
from apps.users.selectors.selectors import get_active_user_by_id

class SelectorTests(TestCase):

    def setUp(self):
        self.active_user = User.objects.create(
            phone_number='09120000000',
            full_name='حسین',
            role=User.Role.CUSTOMER,
            is_active=True
        )
        self.inactive_user = User.objects.create(
            phone_number='09121111111',
            full_name='مینا',
            role=User.Role.STAFF,
            is_active=False
        )

    def test_get_active_user_by_id_success(self):
        user = get_active_user_by_id(self.active_user.id)
        self.assertEqual(user.phone_number, '09120000000')
        self.assertTrue(user.is_active)

    def test_get_active_user_by_id_raises_exception_for_inactive(self):
        with self.assertRaises(User.DoesNotExist):
            get_active_user_by_id(self.inactive_user.id)

    def test_get_active_user_by_id_invalid_id(self):
        with self.assertRaises(User.DoesNotExist):
            get_active_user_by_id(99999)
