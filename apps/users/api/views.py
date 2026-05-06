from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


from apps.users.api.serializers import RegisterSerializer
from apps.users.services.logout_service import logout_service
from apps.users.services.create_user_service import create_user_service


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_user_service(**serializer.validated_data)

        return Response(
    {
        "id": user.id,
        "phone_number": user.phone_number,
        "full_name": user.full_name,
    },
    status=status.HTTP_201_CREATED
)

from django.core.exceptions import ValidationError as DjangoValidationError

from .serializers import LoginSerializer, LogoutSerializer
from apps.users.services.login_user_service import login_user_service
from django.conf import settings


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tokens = login_user_service(
                phone_number=serializer.validated_data["phone_number"],
                password=serializer.validated_data["password"],
            )
        except DjangoValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        refresh = tokens.get("refresh")
        tokens.pop("refresh", None)

        response = Response(tokens, status=status.HTTP_200_OK)
        
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=getattr(settings, "USE_SECURE_COOKIES", False),
            samesite="Strict",
            path="/",
        )

        return response

from .serializers import RefreshTokenSerializer
from apps.users.services.refresh_access_token_service import refresh_access_token_service


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = refresh_access_token_service(
                refresh_token=serializer.validated_data["refresh"]
            )
        except DjangoValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(token, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.api.serializers import VerifyPhoneTokenSerializer
from apps.users.services.verify_phone_token import verify_phone_token

class VerifyPhoneView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyPhoneTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verify_phone_token(serializer.validated_data["token"])

        return Response(
            {"detail": "Phone number verified successfully"},
            status=status.HTTP_200_OK
        )
        
from apps.users.api.serializers import (
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
)
from apps.users.services.password_reset import (
    confirm_password_reset_service,
    request_password_reset_service,
)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_password_reset_service(
            phone_number=serializer.validated_data["phone_number"]
        )

        return Response(
            {"detail": "If this account exists, a reset token has been generated."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            confirm_password_reset_service(
                token=serializer.validated_data["token"],
                new_password=serializer.validated_data["new_password"],
            )
        except DjangoValidationError as e:
            return Response(
                {"detail": e.messages[0] if e.messages else "Invalid request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )

from rest_framework.permissions import IsAuthenticated

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        try:
            logout_service(refresh_token=refresh_token)
        except Exception:
            return Response(
                {"detail": "Invalid refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)