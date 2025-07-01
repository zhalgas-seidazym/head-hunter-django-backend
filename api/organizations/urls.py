from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import IndustryViewSet, IndustryGroupViewSet

router = DefaultRouter()
router.register(r'industries', IndustryViewSet, basename='industry')
router.register(r'industry-groups', IndustryGroupViewSet, basename='industry-group')

urlpatterns = [
    path('', include(router.urls)),
]
