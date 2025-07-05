from django.db import models

class SpecializationGroup(models.Model):
    name = models.CharField(max_length=255)

class Specialization(models.Model):
    name = models.CharField(max_length=255)
    group = models.ForeignKey(SpecializationGroup, on_delete=models.CASCADE, related_name="specializations")

