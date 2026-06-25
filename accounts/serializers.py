from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User, Profile


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

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            phone_number=validated_data["phone_number"],
        )

        Profile.objects.create(
            user=user
        )

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

