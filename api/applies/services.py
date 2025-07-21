from .models import Apply
from ..common.enums import Role, ApplyStatus, MessageStatus


class ApplyService:
    @staticmethod
    def mark_apply_viewed_if_needed(apply: Apply, user):
        if user.role == Role.EMPLOYER and apply.status == ApplyStatus.APPLIED:
            apply.status = ApplyStatus.VIEWED
            apply.save(update_fields=["status"])

    @staticmethod
    def mark_messages_as_read(queryset, user):
        if user.role == Role.APPLICANT:
            queryset.filter(recipient=user, status=MessageStatus.SENT).update(status=MessageStatus.READ)
        elif user.role == Role.EMPLOYER:
            queryset.filter(recipient__isnull=True, status=MessageStatus.SENT).update(status=MessageStatus.READ)