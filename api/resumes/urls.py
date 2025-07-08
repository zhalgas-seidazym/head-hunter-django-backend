from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.resumes.views import *

router = DefaultRouter()

router.register(r"", ResumeViewSet, basename="resume")
router.register(r"experiences", ResumeExperienceViewSet, basename="resume-experience")
router.register(r"educations", ResumeEducationViewSet, basename="resume-education")
router.register(r"courses", ResumeCourseViewSet, basename="resume-course")

urlpatterns = [
    path("", include(router.urls)),
]