from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import *

router = DefaultRouter()
router.register(r'industries', IndustryViewSet, basename='industry')
router.register(r'industry-groups', IndustryGroupViewSet, basename='industry-group')
router.register(r'', OrganizationViewSet, basename='organization')

urlpatterns = [
    path('', include(router.urls)),

    path('join-requests/', CreateJoinRequestApiView.as_view(), name='create-join-request'),
    path('join-requests/my/', GetMyJoinRequestsApiView.as_view(), name='get-my-join-requests'),
    path('join-requests/<int:organization_id>/', ListOrganizationJoinRequestsApiView.as_view(), name='list-join-requests'),
    path('join-requests/<int:organization_id>/status/<int:request_id>/', UpdateJoinRequestStatusApiView.as_view(), name='update-join-request-status'),
]
