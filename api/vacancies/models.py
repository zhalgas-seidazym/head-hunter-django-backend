from django.db import models
from django.conf import settings

from api.common.enums import WorkExperience, EmploymentType, WorkSchedule, WorkFormat, PaymentFrequency, Currency
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
    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.KZT
    )
    is_salary_gross = models.BooleanField(default=True) # without any tax deductions
    payment_frequency = models.CharField(
        max_length=20,
        choices=PaymentFrequency.choices,
        default=PaymentFrequency.MONTHLY
    )

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="vacancies")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="vacancies")

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="vacancies")

    specializations = models.ManyToManyField(Specialization, related_name="vacancies")
    skills = models.ManyToManyField(Skill, blank=True, related_name="vacancies")
    work_experience = models.CharField(
        max_length=20,
        choices=WorkExperience.choices,
        default=WorkExperience.NO_EXPERIENCE
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EmploymentType.choices,
        default=EmploymentType.FULL_TIME
    )
    work_format = models.CharField(
        max_length=20,
        choices=WorkFormat.choices,
        default=WorkFormat.ON_SITE
    )
    work_schedule = models.CharField(
        max_length=25,
        choices=WorkSchedule.choices,
        default=WorkSchedule.FULL_DAY
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
