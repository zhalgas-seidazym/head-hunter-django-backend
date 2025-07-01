from rest_framework.exceptions import ValidationError
from django.db import transaction

from api.common.enums import OrganizationRole
from api.organizations.models import Organization, OrganizationMember


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