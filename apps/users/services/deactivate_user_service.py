from django.db import transaction
from apps.users.models import User


@transaction.atomic
def deactivate_user_service(*, user: User) -> None:

    if not user.is_active:
        return

    user.is_active = False
    user.save(update_fields=["is_active"])