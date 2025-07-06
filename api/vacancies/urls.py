from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.vacancies.views import VacancyViewSet

router = DefaultRouter()
router.register(r'', VacancyViewSet, basename='vacancy')

urlpatterns = [
    path('', include(router.urls)),
]
