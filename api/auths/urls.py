from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import AuthView

router = DefaultRouter()
router.register(r'', AuthView, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # Login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),     # Refresh
]