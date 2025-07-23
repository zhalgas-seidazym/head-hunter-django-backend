from rest_framework import serializers
from .models import Apply, Message
from ..common.enums import ApplyStatus, Role, MessageStatus


class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Apply
        fields = [
            'id',
            'resume',
            'vacancy',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_status(self, status):
        user = self.context['request'].user

        if user.role == Role.EMPLOYER:
            if status not in [ApplyStatus.APPLIED, ApplyStatus.VIEWED, ApplyStatus.OFFER]:
                raise serializers.ValidationError("Employers can only set status to 'applied' or 'offer'.")
        elif user.role == Role.APPLICANT:
            if status != ApplyStatus.APPLIED:
                raise serializers.ValidationError("Applicants can only set status to 'applied'.")
        else:
            raise serializers.ValidationError("Unauthorized role.")

        return status

class ApplyStatusSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=ApplyStatus.choices)

    class Meta:
        model = Apply
        fields = ['status']

    def validate_status(self, new_status):
        user = self.context['request'].user
        instance = self.instance

        current = instance.status
        status_order = ApplyStatus.ordered()

        if current == ApplyStatus.REJECTED:
            raise serializers.ValidationError(
                "This application has been rejected and its status cannot be changed."
            )

        if user.role == Role.EMPLOYER:
            current_index = status_order.index(current)
            new_index = status_order.index(new_status)

            if new_index < current_index:
                raise serializers.ValidationError(
                    f"Cannot change status from '{current}' to '{new_status}': backward transitions are not allowed."
                )

        elif user.role == Role.APPLICANT:
            if new_status != ApplyStatus.WITHDRAWN:
                raise serializers.ValidationError(
                    "Applicants are only allowed to change status to 'withdrawn'."
                )

        else:
            raise serializers.ValidationError("You are not allowed to update the status.")

        return new_status


class MessageSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=MessageStatus.choices, read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'apply',
            'text',
            'sender',
            'recipient',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'apply', 'sender', 'recipient', 'status', 'created_at', 'updated_at']


class UnreadApplySerializer(serializers.Serializer):
    apply = serializers.PrimaryKeyRelatedField(queryset=Apply.objects.all())
    unread_count = serializers.IntegerField()
    latest_message = MessageSerializer()
