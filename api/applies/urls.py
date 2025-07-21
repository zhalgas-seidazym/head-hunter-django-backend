from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include

from api.applies.views import ApplyViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'applies', ApplyViewSet, basename='apply')

applies_router = NestedDefaultRouter(router, r'applies', lookup='apply')
applies_router.register(r'messages', MessageViewSet, basename='apply-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(applies_router.urls)),
]