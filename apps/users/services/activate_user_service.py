from django.db import transaction
from apps.users.models import User


@transaction.atomic
def activate_user_service(*, user: User) -> None:
    
    if user.is_active:
        return 

    user.is_active = True
    user.save(update_fields=["is_active"])