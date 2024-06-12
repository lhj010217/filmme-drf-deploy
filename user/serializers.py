from .models import User
from rest_framework import serializers
from dj_rest_auth.serializers import PasswordChangeSerializer

class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['nickname', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm = serializers.CharField(write_only=True)

class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    origin_password = serializers.CharField(required=True)

# 작성자 본인 확인 api
class CheckWriterSerializer(serializers.ModelSerializer):
    is_writer = serializers.BooleanField(required=True)

    class Meta:
        model = User
        fields = ['is_writer']