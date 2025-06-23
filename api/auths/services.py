import random
import uuid

from django.core.cache import cache
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from api.common.services import send_email_async

User = get_user_model()

class AuthService:

    @staticmethod
    def register(data, session_token):
        email = cache.get(f'session_token:{session_token}')
        if not email or email != data['email']:
            raise ValidationError({"detail": "Session token is expired or invalid."})

        cache.delete(f'session_token:{session_token}')

        return User.objects.create_user(**data)

    @staticmethod
    def send_otp(data):
        email = data['email']
        login = data['login']

        if login:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise NotFound('User not found.')
        else:
            try:
                user = User.objects.get(email=email)
                if user:
                    raise ValidationError('User is already registered.')
            except User.DoesNotExist:
                pass

        otp_code = f"{random.randint(1000, 9999)}"

        message = (
            f"Hello,\n\n"
            f"Your verification code is: {otp_code}\n\n"
            f"If you did not request this code, you can safely ignore this email."
        )

        send_email_async.delay("Verification code", email, message)

        cache.set(f"otp:{otp_code}", email, timeout=300)

    @staticmethod
    def verify_otp(data):
        email = data['email']
        otp_code = data['otp']

        stored_email = cache.get(f"otp:{otp_code}")

        if not stored_email or stored_email != email:
            raise ValidationError({"detail": "OTP code is invalid."})

        cache.delete(f"otp:{otp_code}")

        generate_session_token = uuid.uuid4().hex
        cache.set(f"session_token:{generate_session_token}", email, timeout=600)

        return generate_session_token

    @staticmethod
    def token_by_otp(data):
        email = data['email']
        otp_code = data['otp']

        stored_email = cache.get(f"otp:{otp_code}")

        if not stored_email or stored_email != email:
            raise ValidationError({"detail": "OTP code is invalid."})

        cache.delete(f"otp:{otp_code}")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError({"detail": "User does not exist."})

        refresh = RefreshToken.for_user(user)

        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }