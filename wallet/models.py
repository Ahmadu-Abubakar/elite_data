from django.db import models
from accounts.models import User
from decimal import Decimal


class Wallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wallet"
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00")
    )

# Virtual account credentials
    account_number = models.CharField(
        max_length=10,
        unique=True,
        null=True,
    )

    account_name = models.CharField(
        max_length=100,
        null=True
    )

    bank_name = models.CharField(
        max_length=100,
        null=True
    )

    provider_reference = models.CharField(
        max_length=100,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.email} wallet"
    


# Create your models here.
