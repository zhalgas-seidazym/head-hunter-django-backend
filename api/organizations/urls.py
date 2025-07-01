from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import IndustryViewSet, IndustryGroupViewSet, OrganizationViewSet

router = DefaultRouter()
router.register(r'industries', IndustryViewSet, basename='industry')
router.register(r'industry-groups', IndustryGroupViewSet, basename='industry-group')
router.register(r'', OrganizationViewSet, basename='organization')

urlpatterns = [
    path('', include(router.urls)),
]
