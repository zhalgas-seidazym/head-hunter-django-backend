from rest_framework import serializers

from .models import IndustryGroup, Industry, Organization, OrganizationMember, OrganizationJoinRequest
from ..common.enums import OrganizationRequestStatus, OrganizationRole
from ..locations.models import City
from ..locations.serializers import CitySerializer
from ..users.serializers import UserSerializer


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
            raise serializers.ValidationError("Field 'industry' should not be empty.")
        return value

    def validate(self, attrs):
        if self.instance is None and not attrs.get('industry'):
            raise serializers.ValidationError({
                'industry': "Field 'industry' is mandatory for creating."
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



class OrganizationJoinRequestSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = OrganizationJoinRequest
        fields = ['id', 'organization', 'user', 'status']
        extra_kwargs = {
            'organization': {'required': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        return OrganizationJoinRequest.objects.create(user=user, **validated_data)

    def validate(self, attrs):
        user = self.context['request'].user
        organization = attrs.get('organization')

        existing_request = OrganizationJoinRequest.objects.filter(
            user=user,
            organization=organization,
            status__in=[
                OrganizationRequestStatus.PENDING,
                OrganizationRequestStatus.ACCEPTED,
            ]
        ).first()

        if existing_request:
            raise serializers.ValidationError("You already sent request or accepted.")

        return attrs



class OrganizationJoinRequestManageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    status = serializers.ChoiceField(choices=OrganizationRequestStatus.choices)
    role = serializers.ChoiceField(
        choices=OrganizationRole.choices,
        required=False,
        allow_null=True
    )

    class Meta:
        model = OrganizationJoinRequest
        fields = ['id', 'organization', 'user', 'status', 'role']
        read_only_fields = ['organization', 'user']

    def validate(self, attrs):
        status = attrs.get('status')
        role = attrs.get('role')

        if status == OrganizationRequestStatus.ACCEPTED and not role:
            raise serializers.ValidationError({
                "role": "Show user role when accepting."
            })

        return attrs

