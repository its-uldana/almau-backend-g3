from abc import ABC

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=1, max_length=100)
    new_password = serializers.CharField(min_length=1, max_length=100)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=False, allow_blank=False)


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=1, max_length=100)