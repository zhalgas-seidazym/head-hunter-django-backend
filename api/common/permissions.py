from django.shortcuts import get_object_or_404
from rest_framework import permissions

from api.common.enums import Role, OrganizationRole
from api.organizations.models import OrganizationMember, Organization


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

class CanManageOrganizationJoinRequests(permissions.BasePermission):
    """
    Проверяет, что пользователь — owner или employer в организации с данным pk (organization_pk)
    """

    def has_permission(self, request, view):
        organization_pk = view.kwargs.get('organization_id')

        if not organization_pk:
            return False

        member = OrganizationMember.objects.filter(
            user=request.user,
            organization_id=organization_pk
        ).first()

        if not member:
            return False

        return member.role in (OrganizationRole.OWNER, OrganizationRole.EMPLOYER)

class CanManageVacancy(permissions.BasePermission):
    """
    Доступ разрешён, если:
      1. В теле запроса передан organization (ID).
      2. Ранг роли пользователя в этой организации > 0.
         (OWNER, EMPLOYER, RECRUITER → OK; VIEWER → запрет)
    """

    message = "You don’t have permission to manage vacancies for this organization."

    def has_permission(self, request, view):
        org_id = (
            request.data.get("organization")
            or request.query_params.get("organization")
        )
        if not org_id:
            self.message = "Organization ID is required."
            return False

        try:
            org_id_int = int(org_id)
            organization = get_object_or_404(Organization, pk=org_id_int)
        except (ValueError, TypeError):
            self.message = "Invalid organization ID."
            return False

        member = OrganizationMember.objects.filter(user=request.user,organization=organization).first()
        if member is None:
            self.message = "User does not belong to this organization."
            return False

        return member.has_role_greater_than(OrganizationRole.VIEWER)
