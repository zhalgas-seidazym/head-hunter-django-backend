from .models import Apply
from ..common.enums import Role, ApplyStatus


class ApplyService:
    @staticmethod
    def mark_apply_viewed_if_needed(apply: Apply, user):
        if user.role == Role.EMPLOYER and apply.status == ApplyStatus.APPLIED:
            apply.status = ApplyStatus.VIEWED
            apply.save(update_fields=["status"])