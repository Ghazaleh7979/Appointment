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
    
    
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class VerifyPhoneTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    
class PasswordResetRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)