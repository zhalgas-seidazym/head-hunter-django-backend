from django.db import models


class Role(models.TextChoices):
    APPLICANT = 'applicant', 'Соискатель'
    EMPLOYER = 'employer', 'Работодатель'