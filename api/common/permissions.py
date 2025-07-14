from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from api.common.enums import Role, OrganizationRole
from api.organizations.models import OrganizationMember, Organization
from api.resumes.models import Resume
from api.vacancies.models import Vacancy


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

class IsApplicant(permissions.BasePermission):
    """
    Разрешает доступ, если user.authenticated и его role == APPLICANT
    """
    def has_permission(self, request, view):
        return (
            getattr(request.user, "role", None) == Role.APPLICANT
        )


class IsResumeOwner(permissions.BasePermission):
    """
    Проверяет, что текущий пользователь владелец резюме.

    Работает с:
    - Resume (сам объект)
    - ResumeExperience, ResumeEducation, ResumeCourse (resume — внешний ключ)
    """

    def has_permission(self, request, view):
        if view.action == "create":
            resume_id = request.data.get("resume")
            if not resume_id:
                return False
            try:
                resume = Resume.objects.get(pk=resume_id)
            except Resume.DoesNotExist:
                return False
            return resume.user_id == request.user.id
        return True

    def has_object_permission(self, request, view, obj):
        """
        Проверка для всех retrieve/update/... действий.

        Поддерживает:
        - obj == Resume
        - obj.resume (FK)
        """
        if hasattr(obj, "resume"):
            resume = obj.resume
        elif isinstance(obj, Resume):
            resume = obj
        else:
            return False

        return resume.user_id == request.user.id


class CanManageApply(permissions.BasePermission):
    """
    Global:
        EMPLOYER: can create only if belongs to vacancy's organization
        APPLICANT: can create only with own resume
    Object-level:
        EMPLOYER: can act only if belongs to the organization of the apply's vacancy
        APPLICANT: can act only if owns the resume
    """

    def has_permission(self, request, view):
        data = request.data
        user = request.user

        vacancy_id = data.get('vacancy')
        resume_id = data.get('resume')

        if user.role == Role.EMPLOYER:
            if not vacancy_id:
                raise PermissionDenied("vacancy is required for employers.")

            try:
                vacancy = Vacancy.objects.select_related('organization').get(id=vacancy_id)
            except Vacancy.DoesNotExist:
                raise PermissionDenied("Vacancy not found.")

            if not OrganizationMember.objects.filter(user=user, organization=vacancy.organization).exists():
                raise PermissionDenied("You are not a member of this organization.")

            return True

        elif user.role == Role.APPLICANT:
            if not resume_id:
                raise PermissionDenied("resume is required for applicants.")

            try:
                resume = Resume.objects.select_related('user').get(id=resume_id)
            except Resume.DoesNotExist:
                raise PermissionDenied("Resume not found.")

            if resume.user != user:
                raise PermissionDenied("You can only apply using your own resume.")

            return True

        raise PermissionDenied("Invalid role for this action.")

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == Role.EMPLOYER:
            return OrganizationMember.objects.filter(
                user=user,
                organization=obj.vacancy.organization
            ).exists()

        elif user.role == Role.APPLICANT:
            return obj.resume.user == user

        return False
