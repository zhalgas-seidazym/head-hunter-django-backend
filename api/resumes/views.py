from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.common.mixins import ActionPermissionMixin
from api.common.permissions import IsApplicant, IsResumeOwner
from api.resumes.filters import ResumeFilter
from api.resumes.models import Resume, ResumeExperience, ResumeEducation, ResumeCourse
from api.resumes.serializers import ResumeSerializer, ResumeExperienceSerializer, ResumeEducationSerializer, ResumeCourseSerializer


class ResumeViewSet(ActionPermissionMixin, viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["title", "about"]
    filterset_class = ResumeFilter

    permissions = {
        "create": [IsAuthenticated, IsApplicant],
        "update": [IsAuthenticated, IsResumeOwner],
        "partial_update": [IsAuthenticated, IsResumeOwner],
        "destroy": [IsAuthenticated, IsResumeOwner],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ResumeExperienceViewSet(
    ActionPermissionMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ResumeExperienceSerializer
    queryset = ResumeExperience.objects.all()
    permissions = {
        "create": [IsAuthenticated, IsResumeOwner],
        "update": [IsAuthenticated, IsResumeOwner],
        "partial_update": [IsAuthenticated, IsResumeOwner],
        "destroy": [IsAuthenticated, IsResumeOwner],
    }


class ResumeEducationViewSet(
    ActionPermissionMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ResumeEducationSerializer
    queryset = ResumeEducation.objects.all()
    permissions = {
        "create": [IsAuthenticated, IsResumeOwner],
        "update": [IsAuthenticated, IsResumeOwner],
        "partial_update": [IsAuthenticated, IsResumeOwner],
        "destroy": [IsAuthenticated, IsResumeOwner],
    }


class ResumeCourseViewSet(
    ActionPermissionMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ResumeCourseSerializer
    queryset = ResumeCourse.objects.all()
    permissions = {
        "create": [IsAuthenticated, IsResumeOwner],
        "update": [IsAuthenticated, IsResumeOwner],
        "partial_update": [IsAuthenticated, IsResumeOwner],
        "destroy": [IsAuthenticated, IsResumeOwner],
    }