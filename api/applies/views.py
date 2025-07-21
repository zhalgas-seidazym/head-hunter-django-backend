from rest_framework import viewsets, generics, permissions, mixins
from rest_framework.response import Response

from api.applies.models import Apply
from api.applies.serializers import ApplySerializer, ApplyStatusSerializer
from api.applies.services import ApplyService
from api.common.mixins import ActionPermissionMixin, ActionSerializerMixin
from api.common.permissions import CanManageApply


class ApplyViewSet(
    ActionPermissionMixin,
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
    permissions = {
        "list": [permissions.IsAuthenticated, CanManageApply],
        "create": [permissions.IsAuthenticated, CanManageApply],
        "update": [permissions.IsAuthenticated, CanManageApply],
        "partial_update": [permissions.IsAuthenticated, CanManageApply],
        "retrieve": [permissions.IsAuthenticated, CanManageApply],
    }
    queryset = Apply.objects.all()
    service = ApplyService()

    def get_queryset(self):
        user = self.request.user
        vacancy_id = self.request.query_params.get('vacancy')

        if self.action == "list":
            if vacancy_id:
                return Apply.objects.filter(vacancy__id=vacancy_id)
            else:
                return Apply.objects.filter(resume__user=user)

        return Apply.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.service.mark_apply_viewed_if_needed(instance, request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)