from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.api.serializers import RegisterSerializer
from apps.users.services.create_user_service import create_user_service


class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_user_service(
            phone_number=serializer.validated_data["phone_number"],
            full_name=serializer.validated_data["full_name"],
            password=serializer.validated_data["password"],
        )

        return Response(
            {"id": user.id},
            status=status.HTTP_201_CREATED
        )
