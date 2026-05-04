from typing import Optional

from django.db import transaction

from apps.users.models import User


@transaction.atomic
def create_user_service(
    *,
    phone_number: str,
    full_name: str,
    role: str,
    password: Optional[str] = None,
) -> User:

    user = User.objects.create_user( 
        phone_number=phone_number,
        full_name=full_name,
        role=role,
        password=password,
    )
    return user
