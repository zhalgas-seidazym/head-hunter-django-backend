from rest_framework import viewsets

from api.common.mixins import *


class OrganizationView(viewsets.ModelViewSet, ActionSerializerMixin, ActionPermissionMixin):
    serializers = {

    }
    permissions = {

    }




