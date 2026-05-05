from functools import wraps
from rest_framework.exceptions import PermissionDenied

def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            user = request.user
            roles_ = roles if isinstance(roles, (list, tuple, set)) else [roles]
            if not (user.is_authenticated and getattr(user, "role", None) in roles_):
                raise PermissionDenied("شما دسترسی لازم را ندارید.")
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator
