from django.db import models
from django.contrib.auth.models import AbstractUser 

class User(AbstractUser):

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


    created_at = models.DateTimeField(
        auto_now_add=True
    )

    email_verified = models.BooleanField(default=False)



class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )




class OTP(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "pending"
        ACTIVE  = "ACTIVE", "active"
        CONSUMED = "CONSUMED", "consumed"
        INVALIDATED = "INVALIDATED", "invalidated"

    class Purpose(models.TextChoices):
        EMAIL = "EMAIL", "email_verification"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="otp_code"
    )
    email = models.EmailField()

    purpose = models.CharField(
        max_length=20,
        choices=Purpose.choices
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    otp_code = models.BinaryField()

    attempts_remaining = models.IntegerField(default=5)

    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    consumed_at = models.DateTimeField(null=True, blank=True)



