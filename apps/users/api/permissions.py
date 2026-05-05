from rest_framework.permissions import BasePermission

class IsAdminPermission(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "role", None) == user.Role.ADMIN)
    
    
class IsStaffPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated and
            getattr(user, "role", None) in [user.Role.STAFF, user.Role.ADMIN]
        )
        
class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "id", None) == request.user.id


class IsAdminOrSelfPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and (
                getattr(user, "role", None) == user.Role.ADMIN
                or obj.id == user.id
            )
        )
