from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from django.db import transaction

from api.common.enums import OrganizationRole, OrganizationRequestStatus, ORGANIZATION_ROLE_RANKS
from api.organizations.models import Organization, OrganizationMember, OrganizationJoinRequest


class OrganizationService:
    @staticmethod
    @transaction.atomic
    def create_organization(data: dict, *, creator) -> Organization:
        industry_ids = data.pop("industry", [])

        organization = Organization.objects.create(**data)

        if industry_ids:
            organization.industry.set(industry_ids)

        try:
            OrganizationMember.objects.create(
                user=creator,
                organization=organization,
                role=OrganizationRole.OWNER,
            )
        except Exception as exc:
            raise ValidationError({"detail": str(exc)})

        return organization

    @staticmethod
    def get_my_organization_roles(user):
        return OrganizationMember.objects.filter(user=user)

    @staticmethod
    def quit_organization(organization_pk, user):
        member = OrganizationMember.objects.filter(
            organization_id=organization_pk,
            user=user
        ).first()

        if not member:
            raise ValidationError("You are not a member of the organization.")

        if member.role == OrganizationRole.OWNER:
            raise ValidationError("Owner of the organization can not quit.")

        member.delete()

        accepted_request = OrganizationJoinRequest.objects.filter(
            user=user,
            organization_id=organization_pk,
            status=OrganizationRequestStatus.ACCEPTED
        ).first()

        if accepted_request:
            accepted_request.delete()

        return {"detail": "You have successfully quit the organization."}

class OrganizationJoinRequestService:

    @staticmethod
    def update_request_status(organization_id, request_id, data, current_user):
        new_status = data.get('status', None)
        role = data.get('role', None)

        try:
            join_request = OrganizationJoinRequest.objects.get(
                id=request_id
            )
        except OrganizationJoinRequest.DoesNotExist:
            raise NotFound("Join request not found.")

        if new_status == OrganizationRequestStatus.DECLINED:
            join_request.status = OrganizationRequestStatus.DECLINED
            join_request.save()
            return {"detail": "Join request declined."}

        if new_status != OrganizationRequestStatus.ACCEPTED:
            raise ValidationError("Invalid status.")

        member = OrganizationMember.objects.filter(
            user=current_user,
            organization_id=organization_id
        ).first()

        if not member:
            raise PermissionDenied("You are not in this organization.")

        current_user_rank = ORGANIZATION_ROLE_RANKS.get(member.role)
        target_role_rank = ORGANIZATION_ROLE_RANKS.get(role)

        if target_role_rank is None:
            raise ValidationError("Invalid role.")

        if current_user_rank <= target_role_rank:
            raise ValidationError("You can not assign a role equal or higher than your own.")

        if OrganizationMember.objects.filter(
                user=join_request.user,
                organization_id=organization_id
        ).exists():
            raise ValidationError("User already in organization.")

        join_request.status = OrganizationRequestStatus.ACCEPTED
        join_request.save()

        OrganizationMember.objects.create(
            user=join_request.user,
            organization_id=organization_id,
            role=role
        )

        return {"detail": "User added to organization with role: " + role}