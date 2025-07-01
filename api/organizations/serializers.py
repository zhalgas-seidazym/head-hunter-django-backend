from rest_framework import serializers

from .models import IndustryGroup, Industry, Organization, OrganizationMember
from ..locations.models import City
from ..locations.serializers import CitySerializer


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'name', 'group']

class IndustryGroupSerializer(serializers.ModelSerializer):
    industries = IndustrySerializer(many=True, read_only=True)

    class Meta:
        model = IndustryGroup
        fields = ['id', 'name', 'industries']



class OrganizationSerializer(serializers.ModelSerializer):
    industry = serializers.PrimaryKeyRelatedField(
        queryset=Industry.objects.all(),
        many=True,
        write_only=True,
        required=False
    )
    industry_data = IndustrySerializer(many=True, read_only=True, source='industry')

    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )
    city_data = CitySerializer(read_only=True, source='city')


    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'description', 'industry', 'industry_data', 'website',
            'email', 'phone', 'city', 'city_data', 'address', 'logo'
        ]
        extra_kwargs = {
            'name': {'required': True},
        }

    def validate_industry(self, value):
        if not value:
            raise serializers.ValidationError("Поле 'industry' обязательно и не может быть пустым.")
        return value

    def validate(self, attrs):
        if self.instance is None and not attrs.get('industry'):
            raise serializers.ValidationError({
                'industry': "Поле 'industry' обязательно при создании."
            })
        return attrs

class OrganizationMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationMember
        fields = [
            'id',
            'user',
            'organization',
            'role',
            'invited_by',
        ]
        read_only_fields = fields