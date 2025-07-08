from django.db import models
from django.conf import settings

from api.common.enums import Currency, EducationDegree
from api.common.models import BaseModel
from api.locations.models import City
from api.organizations.models import Industry
from api.skills.models import Skill
from api.specializations.models import Specialization


class Resume(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes")

    title = models.CharField(max_length=255)
    about = models.TextField()
    expected_salary = models.IntegerField()
    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        default=Currency.KZT
    )

    phone = models.CharField(max_length=20)
    email = models.EmailField()

    employment_types = models.JSONField(default=list, blank=True)
    work_schedules = models.JSONField(default=list, blank=True)
    work_formats = models.JSONField(default=list, blank=True)
    payment_frequencies = models.JSONField(default=list, blank=True)

    skills = models.ManyToManyField(Skill, blank=True, related_name="resumes")
    specializations = models.ManyToManyField(Specialization, related_name="resumes")

    def __str__(self):
        return f"{self.title} — {self.user}"


class ResumeExperience(BaseModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="experiences")

    company_name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name="company_experiences")
    company_website = models.URLField(blank=True, null=True)

    industries = models.ManyToManyField(Industry, blank=True, related_name="experience_entries")
    specializations = models.ManyToManyField(Specialization, blank=True, related_name="experience_entries")

    start_month = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 13)])
    start_year = models.PositiveSmallIntegerField()

    currently_working = models.BooleanField(default=False)

    end_month = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 13)], null=True, blank=True)
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)

    responsibilities = models.TextField(blank=True)


    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.currently_working and (self.end_month is None or self.end_year is None):
            raise ValidationError("End date is required if not currently working.")

    def __str__(self):
        return f"{self.company_name} — {self.start_month}/{self.start_year}"


class ResumeEducation(BaseModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="educations")

    degree = models.CharField(
        max_length=30,
        choices=EducationDegree.choices
    )
    institution_name = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    graduation_year = models.PositiveSmallIntegerField(blank=True, null=True)  # Можно не заполнять, если учится


    def __str__(self):
        return f"{self.institution_name} — {self.get_degree_display()}"
