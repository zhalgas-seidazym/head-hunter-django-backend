from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    login = serializers.BooleanField()

class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'password', 'password2', 'phone', 'role', 'avatar', 'city', 'birth_date']
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'surname': {'required': True},
            'role': {'required': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2', None)

        if password != password2:
            raise serializers.ValidationError('Passwords must match.')

        return attrs