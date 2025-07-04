from rest_framework import viewsets, generics, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema

from api.common.mixins import *
from api.common.permissions import IsEmployer, IsOrganizationOwner, CanManageOrganizationJoinRequests
from api.organizations.serializers import *
from api.organizations.services import OrganizationService, OrganizationJoinRequestService


@extend_schema_view(
    list=extend_schema(tags=["Industries"], description="List of industries"),
    retrieve=extend_schema(tags=["Industries"], description="Retrieve single industry"),
)
class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer


@extend_schema_view(
    list=extend_schema(tags=["Industries"], description="List of industry groups with industries"),
    retrieve=extend_schema(tags=["Industries"], description="Retrieve single industry group with industries"),
)
class IndustryGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndustryGroup.objects.prefetch_related('industries').all()
    serializer_class = IndustryGroupSerializer


@extend_schema_view(
    create=extend_schema(tags=["Organizations"], description="Create an organization"),
    update=extend_schema(tags=["Organizations"], description="Update an organization"),
    list=extend_schema(tags=["Organizations"], description="List organizations"),
    retrieve=extend_schema(tags=["Organizations"], description="Retrieve an organization"),
    partial_update=extend_schema(tags=["Organizations"], description="Partially update an organization"),
    destroy=extend_schema(tags=["Organizations"], description="Delete an organization"),
    my_organization_roles=extend_schema(tags=["Organizations"], description="My organization roles"),
    quit_organization=extend_schema(tags=["Organizations"], description="Quit an organization"),
    organization_roles=extend_schema(tags=["Organizations"], description="Organization roles"),
)
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
        "organization_roles": (IsAuthenticated, IsEmployer),
        "quit_organization": (IsAuthenticated, IsEmployer),
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

    @action(detail=False, methods=['get'], url_path='roles')
    def organization_roles(self, request, *args, **kwargs):
        roles = [
            {"value": choice[0], "label": choice[1]}
            for choice in OrganizationRole.choices
        ]
        return Response(roles, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='my-roles')
    def my_organization_roles(self, request, *args, **kwargs):
        members = self.service.get_my_organization_roles(request.user)
        serializer = self.get_serializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='quit')
    def quit_organization(self, request, *args, **kwargs):
        response = self.service.quit_organization(kwargs["pk"], request.user)

        return Response(response, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(tags=["Organization Join Requests"], description="Create a join request to organization"),
)
class CreateJoinRequestApiView(generics.CreateAPIView):
    serializer_class   = OrganizationJoinRequestSerializer
    permission_classes = [IsAuthenticated, IsEmployer]


@extend_schema_view(
    get=extend_schema(tags=["Organization Join Requests"], description="Get your join requests to organizations"),
)
class GetMyJoinRequestsApiView(generics.ListAPIView):
    serializer_class   = OrganizationJoinRequestSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        return OrganizationJoinRequest.objects.filter(user=self.request.user).order_by("-created_at")


@extend_schema_view(
    get=extend_schema(tags=["Organization Join Requests"], description="Get join requests to organization"),
)
class ListOrganizationJoinRequestsApiView(generics.ListAPIView):
    serializer_class   = OrganizationJoinRequestManageSerializer
    permission_classes = [IsAuthenticated, CanManageOrganizationJoinRequests]
    queryset = OrganizationJoinRequest.objects.all()

    def get_queryset(self):
        organization_id = self.kwargs["organization_id"]
        return OrganizationJoinRequest.objects.filter(
            organization_id=organization_id,
            status=OrganizationRequestStatus.PENDING
        )


@extend_schema_view(
    put=extend_schema(tags=["Organization Join Requests"], description="Update a join request status to organization"),
    patch=extend_schema(tags=["Organization Join Requests"], description="Partial update a join request status to organization"),
)
class UpdateJoinRequestStatusApiView(generics.UpdateAPIView):
    serializer_class   = OrganizationJoinRequestManageSerializer
    permission_classes = [IsAuthenticated, CanManageOrganizationJoinRequests]
    lookup_url_kwarg   = "request_id"

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = OrganizationJoinRequestService.update_request_status(
            organization_id = kwargs["organization_id"],
            request_id      = kwargs[self.lookup_url_kwarg],
            data            = serializer.validated_data,
            current_user    = request.user,
        )
        return Response(response, status=status.HTTP_200_OK)

