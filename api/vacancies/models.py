from django.db import models
from django.conf import settings

from api.common.enums import WorkExperience
from api.common.models import BaseModel
from api.locations.models import City
from api.organizations.models import Organization
from api.skills.models import Skill
from api.specializations.models import Specialization


class Vacancy(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    salary_from = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_to = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_salary_gross = models.BooleanField(default=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="vacancies")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="vacancies")

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="vacancies")
    remote = models.BooleanField(default=False)

    specializations = models.ManyToManyField(Specialization, blank=True, related_name="vacancies")
    skills = models.ManyToManyField(Skill, blank=True, related_name="vacancies")
    work_experience = models.CharField(
        max_length=20,
        choices=WorkExperience.choices,
        default=WorkExperience.NO_EXPERIENCE
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
