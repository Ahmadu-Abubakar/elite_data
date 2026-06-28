from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Profile

from wallet.services import create_wallet, WalletAlreadyExistsError
from django.db import transaction



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "phone_number",
        ]

        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate_email(self, value):
        value = value.strip().lower()

        if "admin" in value:
            raise serializers.ValidationError(
                "Email cannot contain admin."
            )

        return value

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):

       with transaction.atomic():

            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
                phone_number=validated_data["phone_number"],
            )

            try:
                create_wallet(user)
            except WalletAlreadyExistsError as e:
                return str(e)
            return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False
    )


class RefreshTokenSerializer(
    serializers.Serializer
):
    refresh_token = serializers.CharField()

