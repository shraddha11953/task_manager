from rest_framework.permissions import BasePermission
from users.models import Role


def get_user_role(user):
    try:
        return Role.objects.get(user=user).role
    except Role.DoesNotExist:
        return None


# ----------------------------------------
# PERMISSION: ADMIN ONLY
# ----------------------------------------
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == "Admin"


# ----------------------------------------
# PERMISSION: ADMIN OR MANAGER
# ----------------------------------------
class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        role = get_user_role(request.user)
        return role in ["Admin", "Manager"]


# ----------------------------------------
# PERMISSION: EMPLOYEE (only see own tasks)
# ----------------------------------------
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == "Employee"
