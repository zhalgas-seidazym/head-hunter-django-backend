from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view

from api.specializations.models import Specialization, SpecializationGroup
from api.specializations.serializers import SpecializationSerializer, SpecializationGroupSerializer


@extend_schema_view(
    list=extend_schema(tags=["Specializations"], description="List of specializations"),
    retrieve=extend_schema(tags=["Specializations"], description="Retrieve single specialization"),
)
class SpecializationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer


@extend_schema_view(
    list=extend_schema(tags=["Specializations"], description="List of industry groups with specializations"),
    retrieve=extend_schema(tags=["Specializations"], description="Retrieve single industry group with specializations"),
)
class SpecializationGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SpecializationGroup.objects.prefetch_related('specializations').all()
    serializer_class = SpecializationGroupSerializer
