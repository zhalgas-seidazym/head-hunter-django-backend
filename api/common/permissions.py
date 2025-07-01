from rest_framework import permissions

from api.common.enums import Role, OrganizationRole
from api.organizations.models import OrganizationMember


class IsEmployer(permissions.BasePermission):
    """
    Разрешает доступ, если user.authenticated и его role == EMPLOYER
    """
    def has_permission(self, request, view):
        return (
            getattr(request.user, "role", None) == Role.EMPLOYER
        )

class IsOrganizationOwner(permissions.BasePermission):
    """
    Доступ только если user — владелец (OWNER) организации.
    Работает с actions, где передаётся /organizations/<id>/
    """

    def has_permission(self, request, view):
        if not hasattr(view, 'action') or view.action not in ('update', 'partial_update', 'destroy'):
            return True

        org_id = view.kwargs.get('pk')

        if not org_id:
            return False

        return OrganizationMember.objects.filter(
            user=request.user,
            organization_id=org_id,
            role=OrganizationRole.OWNER
        ).exists()
