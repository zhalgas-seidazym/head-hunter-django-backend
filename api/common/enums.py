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

class WorkExperience(models.TextChoices):
    NO_EXPERIENCE = "no_experience", "Нет опыта"
    LESS_THAN_ONE = "less_than_one", "Меньше года"
    ONE_TO_THREE = "one_to_three", "От 1 года до 3 лет"
    THREE_TO_FIVE = "three_to_five", "От 3 до 5 лет"
    MORE_THAN_FIVE = "more_than_five", "Более 5 лет"
