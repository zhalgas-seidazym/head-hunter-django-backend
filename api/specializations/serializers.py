from rest_framework import serializers

from api.specializations.models import Specialization, SpecializationGroup


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name', 'group']

class SpecializationGroupSerializer(serializers.ModelSerializer):
    specialization = SpecializationSerializer(many=True, read_only=True)

    class Meta:
        model = SpecializationGroup
        fields = ['id', 'name', 'specialization']
