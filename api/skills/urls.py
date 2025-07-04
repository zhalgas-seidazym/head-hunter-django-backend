from django.urls import path, include

from .views import *

urlpatterns = [
    path('', ListCreateSkillsAPIView.as_view(), name='list-create-skills-api'),
]
