from apps.users.models import User
from django.db import transaction


@transaction.atomic
def change_password_service(
    *,
    user: User,
    new_password: str,
) -> None:
    user.set_password(new_password)  
    user.save(update_fields=["password"])  