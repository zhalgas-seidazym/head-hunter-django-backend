from django.db import models

from api.common.enums import ApplyStatus
from api.common.models import BaseModel
from api.resumes.models import Resume
from api.vacancies.models import Vacancy


class Apply(BaseModel):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='applies')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applies')

    status = models.CharField(
        max_length=20,
        choices=ApplyStatus.choices,
        default=ApplyStatus.APPLIED
    )


    class Meta:
        unique_together = ('resume', 'vacancy')

    def __str__(self):
        return f'{self.resume} → {self.vacancy} ({self.status})'
