from rest_framework.routers import DefaultRouter
from django.urls import path, include

from api.applies.views import ApplyViewSet

router = DefaultRouter()
router.register(r'', ApplyViewSet, basename='apply')

urlpatterns = [
    path('', include(router.urls)),
]