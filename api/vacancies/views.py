from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters

from api.common.permissions import CanManageVacancy
from api.vacancies.models import Vacancy
from api.vacancies.serializers import VacancySerializer
from api.common.mixins import ActionPermissionMixin

class VacancyViewSet(ActionPermissionMixin, viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "description"]


    permissions = {
        "list": [permissions.AllowAny],
        "retrieve": [permissions.AllowAny],
        "create": [permissions.IsAuthenticated, CanManageVacancy],
        "update": [permissions.IsAuthenticated, CanManageVacancy],
        "partial_update": [permissions.IsAuthenticated, CanManageVacancy],
        "destroy": [permissions.IsAuthenticated, CanManageVacancy],
    }

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
