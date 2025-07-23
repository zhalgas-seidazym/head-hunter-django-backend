from rest_framework import viewsets, permissions, mixins, views
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.applies.models import Apply, Message
from api.applies.serializers import ApplySerializer, ApplyStatusSerializer, MessageSerializer, UnreadApplySerializer
from api.applies.services import ApplyService, MessageService
from api.common.enums import Role
from api.common.mixins import ActionSerializerMixin
from api.common.permissions import CanManageApply
from api.organizations.models import OrganizationMember


@extend_schema_view(
    list=extend_schema(tags=['Applies'], description='List Apply objects'),
    create=extend_schema(tags=['Applies'], description='Create Apply objects'),
    update=extend_schema(tags=['Applies'], description='Update Apply objects'),
    partial_update=extend_schema(tags=['Applies'], description='Partial Update Apply objects'),
    retrieve=extend_schema(tags=['Applies'], description='Get Apply objects'),
)
class ApplyViewSet(
    ActionSerializerMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializers = {
        "list": ApplySerializer,
        "create": ApplySerializer,
        "update": ApplyStatusSerializer,
        "partial_update": ApplyStatusSerializer,
        "retrieve": ApplySerializer,
    }
    permission_classes = [permissions.IsAuthenticated, CanManageApply]
    queryset = Apply.objects.all()
    service = ApplyService()

    def get_queryset(self):
        user = self.request.user
        org_id = self.request.query_params.get('organization')

        if self.action == "list":
            if user.role == Role.EMPLOYER:
                if not org_id:
                    return Apply.objects.none()

                if not OrganizationMember.objects.filter(user=user, organization_id=org_id).exists():
                    return Apply.objects.none()

                queryset = Apply.objects.filter(vacancy__organization_id=org_id)

                return queryset

            elif user.role == Role.APPLICANT:
                return Apply.objects.filter(resume__user=user)

            return Apply.objects.none()

        return Apply.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.service.mark_apply_viewed_if_needed(instance, request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(tags=['Apply Messages'], description='List apply message objects'),
    create=extend_schema(tags=['Apply Messages'], description='Create apply message object'),
)
class MessageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageApply]

    service = MessageService()

    def get_queryset(self):
        apply_id = self.kwargs['apply_pk']
        return Message.objects.filter(apply_id=apply_id).order_by('-created_at')

    def perform_create(self, serializer):
        apply_id = self.kwargs.get('apply_pk')
        apply = Apply.objects.select_related('resume__user').get(id=apply_id)
        user = self.request.user

        if user.role == Role.EMPLOYER:
            recipient = apply.resume.user
        elif user.role == Role.APPLICANT:
            recipient = None
        else:
            raise PermissionDenied("Invalid user role for sending message.")

        serializer.save(
            sender=user,
            recipient=recipient,
            apply=apply
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        self.service.mark_messages_as_read(queryset, request.user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UnreadMessagesSummaryView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    service = MessageService()

    @extend_schema(
        tags=["Apply Messages"],
        description="Get count of unread messages.",
        responses={200: OpenApiResponse(UnreadApplySerializer(many=True))}
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        organization_id = request.query_params.get("organization")
        data = MessageService.get_unread_summary(user, organization_id)
        serializer = UnreadApplySerializer(data, many=True)
        return Response(serializer.data)
