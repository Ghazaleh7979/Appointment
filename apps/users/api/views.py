from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.api.serializers import RegisterSerializer
from apps.users.services.create_user_service import create_user_service


class RegisterView(APIView):

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

from .serializers import LoginSerializer
from apps.users.services.login_user_service import login_user_service


class LoginView(APIView):
    permission_classes = []

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

        return Response(tokens, status=status.HTTP_200_OK)

from .serializers import RefreshTokenSerializer
from apps.users.services.refresh_access_token_service import refresh_access_token_service


class RefreshTokenView(APIView):
    permission_classes = []

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
