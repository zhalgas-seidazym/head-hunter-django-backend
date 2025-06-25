from django.db import models
from django.contrib.auth import get_user_model

from api.common.models import BaseModel
from api.locations.models import City
from api.common.enums import OrganizationRole, ORGANIZATION_ROLE_RANKS, OrganizationRequestStatus

User = get_user_model()

class IndustryGroup(models.Model):
    name = models.CharField(max_length=255)

class Industry(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(IndustryGroup, on_delete=models.CASCADE, related_name="industries")

class Organization(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    industry = models.ManyToManyField("Industry", blank=True, related_name="organizations")
    website = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL, related_name='organization_city')
    address = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    def __str__(self):
        return self.name


class OrganizationMember(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=OrganizationRole.choices)
    invited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='invitations')

    class Meta:
        unique_together = ('user', 'organization')

    def role_rank(self):
        return ORGANIZATION_ROLE_RANKS.get(self.role, -1)

    def has_role_greater_than(self, min_role):
        return self.role_rank() >= ORGANIZATION_ROLE_RANKS[min_role]


class OrganizationJoinRequest(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='join_requests')
    status = models.CharField(max_length=20, choices=OrganizationRequestStatus.choices, default=OrganizationRequestStatus.PENDING)

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return f"{self.user} → {self.organization} ({self.status})"
