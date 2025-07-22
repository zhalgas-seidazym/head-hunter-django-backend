from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view

from api.users.serializers import UserSerializer

User = get_user_model()


@extend_schema_view(
    me=extend_schema(tags=["Users"], description="Get, update, delete user."),
    role=extend_schema(tags=["Users"], description="Get user role."),
)
class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'patch', 'put', 'delete'], url_path='me')
    def me(self, request):
        """
        GET: get current user
        PATCH: partially update current user
        PUT: fully update current user
        DELETE: delete current user
        """
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        elif request.method in ['PATCH', 'PUT']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(user, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'DELETE':
            user.delete()
            return Response({"detail": "User deleted."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='role')
    def role(self, request):
        """
        GET: return current user's role
        """
        return Response({'role': request.user.role})
