from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.auths.serializers import SendOtpSerializer, VerifyOtpSerializer, RegisterSerializer
from api.auths.services import AuthService
from api.common.mixins import ActionSerializerMixin
from api.users.models import User


class AuthView(ActionSerializerMixin, GenericViewSet):
    serializers = {
        "send_otp": SendOtpSerializer,
        "verify_otp": VerifyOtpSerializer,
        "token_by_otp": VerifyOtpSerializer,
        "register": RegisterSerializer,
    }

    service = AuthService()
    queryset = User.objects.none()

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request, *args, **kwargs):
        session_token = request.COOKIES.get("SESSION-TOKEN")

        if not session_token:
            return Response(
                {"detail": "Session token is missing or invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.service.register(serializer.validated_data, session_token)

        return Response({"detail": "User created."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="send-otp")
    def send_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, *args, **kwargs)
        serializer.is_valid(raise_exception=True)
        self.service.send_otp(serializer.validated_data)
        return Response({"detail": "OTP sent successfully"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="verify-otp")
    def verify_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, *args, **kwargs)
        serializer.is_valid(raise_exception=True)
        session_token = self.service.verify_otp(serializer.validated_data)

        response = Response(
            {"detail": "OTP verified successfully."},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="SESSION-TOKEN",
            value=session_token,
            httponly=True,
            secure=True,
            max_age=3600,
            samesite="None"
        )
        return response

    @action(detail=False, methods=["post"], url_path="token-by-otp")
    def token_by_otp(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, *args, **kwargs)
        serializer.is_valid(raise_exception=True)

        token = self.service.token_by_otp(serializer.validated_data)

        return Response({
            'access_token': token.access,
            'refresh_token': token.refresh,
        }, status=status.HTTP_200_OK)
