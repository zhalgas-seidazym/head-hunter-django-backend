from django.db.models.aggregates import Max, Count
from rest_framework.exceptions import ValidationError, PermissionDenied

from .models import Apply, Message
from ..common.enums import Role, ApplyStatus, MessageStatus
from ..organizations.models import OrganizationMember


class ApplyService:
    @staticmethod
    def mark_apply_viewed_if_needed(apply: Apply, user):
        if user.role == Role.EMPLOYER and apply.status == ApplyStatus.APPLIED:
            apply.status = ApplyStatus.VIEWED
            apply.save(update_fields=["status"])


class MessageService:
    @staticmethod
    def mark_messages_as_read(queryset, user):
        if user.role == Role.APPLICANT:
            queryset.filter(recipient=user, status=MessageStatus.SENT).update(status=MessageStatus.READ)
        elif user.role == Role.EMPLOYER:
            queryset.filter(recipient__isnull=True, status=MessageStatus.SENT).update(status=MessageStatus.READ)


    @staticmethod
    def get_unread_summary(user, organization_id=None):
        if user.role == Role.EMPLOYER:
            if not organization_id:
                raise ValidationError("Organization ID is required for employers.")

            if not OrganizationMember.objects.filter(user=user, organization_id=organization_id).exists():
                raise PermissionDenied("You are not a member of this organization.")

            apply_ids = Apply.objects.filter(
                vacancy__organization_id=organization_id
            ).values_list('id', flat=True)

            messages = Message.objects.filter(
                apply_id__in=apply_ids,
                recipient__isnull=True,
                status=MessageStatus.SENT
            )

        elif user.role == Role.APPLICANT:
            messages = Message.objects.filter(
                recipient=user,
                status=MessageStatus.SENT
            )
        else:
            raise PermissionDenied("Invalid user role.")

        summary = (
            messages.values('apply')
            .annotate(
                unread_count=Count('id'),
                latest_id=Max('id')
            )
        )

        latest_ids = [item['latest_id'] for item in summary]
        latest_messages = Message.objects.filter(id__in=latest_ids)
        messages_map = {msg.id: msg for msg in latest_messages}

        result = []
        for item in summary:
            msg = messages_map.get(item['latest_id'])
            if msg:
                result.append({
                    'apply': msg.apply,
                    'unread_count': item['unread_count'],
                    'latest_message': msg
                })

        return result
