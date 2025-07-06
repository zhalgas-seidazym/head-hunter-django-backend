from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.specializations.views import SpecializationViewSet, SpecializationGroupViewSet

router = DefaultRouter()
router.register(r'', SpecializationViewSet, basename='specialization')
router.register(r'groups', SpecializationGroupViewSet, basename='specialization-group')

urlpatterns = [
    path('', include(router.urls)),
]
