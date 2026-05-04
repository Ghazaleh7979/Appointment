from rest_framework import serializers
from apps.users.models import User


class RegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    full_name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number already exists")
        return value
