from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from . import res_codes

class IsAdmin(BasePermission):
    message = 'You are not allowed to view this page.'
    """
    Admin only
    """
    def has_permission(self, request, view):
        if not int(request.user.profile.role) == 3:
            raise PermissionDenied(
                res_codes.get_response_dict(res_codes.NO_ACCESS)
            )
        return True

