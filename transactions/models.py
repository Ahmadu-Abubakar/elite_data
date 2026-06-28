from django.db import models
from wallet.models import Wallet
import uuid



class Transaction(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING" , "pending"
        SUCCESS = "SUCCESS" , "success"
        FAILED = "FAILED" , "failure"
        
    class Type(models.TextChoices):
        DEPOSIT = "DEPOSIT" , "deposit", 
        BUY_DATA = "BUY_DATA", "data plan"
        BUY_AIRTIME = "BUY_AIRTIME", "airtime"


    class TelecomProviders(models.TextChoices):
        MTN = "MTN" , "mtn network", 
        AIRTEL = "AIRTEL", "airtel network"
        GLO = "GLO", "glo network"
        NINE_MOBILE = "9MOBIL", "9mobile network"

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    transaction_type = models.CharField(
        max_length=40,
        choices=Type.choices,
        
    )


    references = models.UUIDField(
        editable=False,
        default=uuid.uuid4,
        unique=True
    )

    telecom_providers = models.CharField(
        max_length=50,
        choices=TelecomProviders.choices,
        null=True,
        blank=True
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



# Create your models here.
