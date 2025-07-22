from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.users.views import UserViewSet

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls))
]