from rest_framework import serializers
from .models import User


class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ["id", "username", "first_name", "last_name", "password", "email", "phone_number"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create_user(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data["last_name"],
            phone_number=validated_data['phone_number'],
        )

        return user
