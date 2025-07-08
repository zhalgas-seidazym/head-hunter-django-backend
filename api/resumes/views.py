from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema

from api.common.mixins import ActionPermissionMixin
from api.common.permissions import IsApplicant, IsResumeOwner
from api.resumes.filters import ResumeFilter
from api.resumes.models import Resume, ResumeExperience, ResumeEducation, ResumeCourse
from api.resumes.serializers import ResumeSerializer, ResumeExperienceSerializer, ResumeEducationSerializer, ResumeCourseSerializer


@extend_schema_view(
    list=extend_schema(tags=['Resumes'], description="List resumes by filters"),
    retrieve=extend_schema(tags=['Resumes'], description="Get resume by id"),
    create=extend_schema(tags=['Resumes'], description="Create resume"),
    update=extend_schema(tags=['Resumes'], description="Update resume"),
    partial_update=extend_schema(tags=['Resumes'], description="Partial update resume"),
    destroy=extend_schema(tags=['Resumes'], description="Delete resume"),
)
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


@extend_schema_view(
    create=extend_schema(tags=['Resume Experiences'], description="Create resume experience"),
    update=extend_schema(tags=['Resume Experiences'], description="Update resume experience"),
    partial_update=extend_schema(tags=['Resume Experiences'], description="Partial update resume experience"),
    destroy=extend_schema(tags=['Resume Experiences'], description="Delete resume experience"),
)
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


@extend_schema_view(
    create=extend_schema(tags=['Resume Educations'], description="Create resume education"),
    update=extend_schema(tags=['Resume Educations'], description="Update resume education"),
    partial_update=extend_schema(tags=['Resume Educations'], description="Partial update resume education"),
    destroy=extend_schema(tags=['Resume Educations'], description="Delete resume education"),
)
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


@extend_schema_view(
    create=extend_schema(tags=['Resume Courses'], description="Create resume course"),
    update=extend_schema(tags=['Resume Courses'], description="Update resume course"),
    partial_update=extend_schema(tags=['Resume Courses'], description="Partial update resume course"),
    destroy=extend_schema(tags=['Resume Courses'], description="Delete resume course"),
)
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