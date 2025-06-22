from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from api.users.models import User
from api.users.serializers import UserSerializer

# class RegisterApiView(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
