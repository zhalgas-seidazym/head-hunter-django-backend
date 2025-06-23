from django.db import models


class Role(models.TextChoices):
    APPLICANT = 'applicant', 'Соискатель'
    EMPLOYER = 'employer', 'Работодатель'


class OrganizationRole(models.TextChoices):
    OWNER = 'owner', 'Owner'
    EMPLOYER = 'employer', 'Employer'
    RECRUITER = 'recruiter', 'Recruiter'
    VIEWER = 'viewer', 'Viewer'

ORGANIZATION_ROLE_RANKS = {
    OrganizationRole.OWNER: 3,
    OrganizationRole.EMPLOYER: 2,
    OrganizationRole.RECRUITER: 1,
    OrganizationRole.VIEWER: 0,
}


class OrganizationRequestStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    DECLINED = 'declined', 'Declined'
