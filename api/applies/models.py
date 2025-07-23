from django.db import models
from django.contrib.auth import get_user_model

from api.common.enums import ApplyStatus, MessageStatus
from api.common.models import BaseModel
from api.resumes.models import Resume
from api.vacancies.models import Vacancy



User = get_user_model()

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


class Message(BaseModel):
    apply = models.ForeignKey(
        Apply,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='received_messages',
        null=True,
        blank=True,
        help_text="Can be null if message is for any employer in the organization"
    )

    text = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=MessageStatus.choices,
        default=MessageStatus.SENT
    )


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} → {self.recipient or 'organization'}: {self.text[:30]}"
