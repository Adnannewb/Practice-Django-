from rest_framework.permissions import BasePermission


class IsManager(BasePermission):

    message = "Only managers can access this resource."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        try:
            return request.user.employee_profile.role == 'manager'
        except Exception:
            return False