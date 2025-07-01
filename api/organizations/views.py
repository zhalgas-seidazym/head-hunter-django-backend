from rest_framework import viewsets

from api.common.mixins import *
from api.organizations.serializers import *


class IndustryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class IndustryGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IndustryGroup.objects.prefetch_related('industries').all()
    serializer_class = IndustryGroupSerializer


class OrganizationView(viewsets.ModelViewSet, ActionSerializerMixin, ActionPermissionMixin):
    serializers = {

    }
    permissions = {

    }




