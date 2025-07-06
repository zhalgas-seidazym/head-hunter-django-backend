from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework import permissions
from drf_spectacular.utils import extend_schema_view, extend_schema

from api.common.mixins import MethodPermissionMixin
from api.skills.models import Skill
from api.skills.serializers import SkillSerializer


@extend_schema_view(
    get=extend_schema(tags=["Skills"], description="Get skills list."),
    post=extend_schema(tags=["Skills"], description="Get existing skill or create new one."),
)
class ListCreateSkillsAPIView(MethodPermissionMixin, generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permissions = {
        'post': [permissions.IsAuthenticated],
        'get': [permissions.AllowAny]
    }

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get('name').strip().lower().capitalize()

        skill, created = Skill.objects.get_or_create(name=name)

        output_serializer = self.get_serializer(skill)
        return Response(output_serializer.data, status=201 if created else 200)
