from rest_framework import serializers
from .models import IndustryGroup, Industry

class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name', 'group']

class IndustryGroupSerializer(serializers.ModelSerializer):
    industries = IndustrySerializer(many=True, read_only=True)

    class Meta:
        model = IndustryGroup
        fields = ['id', 'name', 'industries']