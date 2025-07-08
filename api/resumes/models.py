from django.db import models
from django.conf import settings

from api.common.enums import Currency
from api.skills.models import Skill
from api.specializations.models import Specialization


class Resume(models.Model):
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
    specializations = models.ManyToManyField(Specialization, related_name="vacancies")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.user}"