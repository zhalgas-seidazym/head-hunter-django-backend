from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema


from api.common.mixins import *
from api.common.permissions import IsEmployer, IsOrganizationOwner
from api.organizations.serializers import *
from api.organizations.services import OrganizationService


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class IndustryGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndustryGroup.objects.prefetch_related('industries').all()
    serializer_class = IndustryGroupSerializer

class OrganizationViewSet(
    ActionSerializerMixin,
    ActionPermissionMixin,
    viewsets.ModelViewSet,
):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    serializers = {
        "create": OrganizationSerializer,
        "list": OrganizationSerializer,
        "retrieve": OrganizationSerializer,
        "update": OrganizationSerializer,
        "partial_update": OrganizationSerializer,
        "destroy": OrganizationSerializer,
        "my_organization_roles": OrganizationMemberSerializer,
    }
    permissions = {
        "list": (),
        "retrieve": (),
        "create": (IsAuthenticated, IsEmployer),
        "update": (IsAuthenticated, IsOrganizationOwner),
        "partial_update": (IsAuthenticated, IsOrganizationOwner),
        "destroy": (IsAuthenticated, IsOrganizationOwner),
        "my_organization_roles": (IsAuthenticated, IsEmployer),
    }

    service = OrganizationService()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        org = self.service.create_organization(
            data=serializer.validated_data,
            creator=self.request.user,
        )
        serializer.instance = org

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='my-organization-roles')
    def my_organization_roles(self, request, *args, **kwargs):
        members = self.service.get_my_organization_roles(request.user)
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


