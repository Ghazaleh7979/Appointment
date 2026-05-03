from apps.users.models import User


def get_user_by_phone(phone_number: str) -> User:
    return User.objects.get(phone_number=phone_number)

def get_active_user_by_id(user_id: int) -> User:
    return User.objects.get(id=user_id, is_active=True)