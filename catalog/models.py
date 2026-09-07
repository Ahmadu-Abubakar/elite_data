from django.db import models



class Catalog(models.Model):

    class ProductState(models.TextChoices):
        AVAILABLE = "AVAILABLE", "available"
        UNAVAILABLE = "UNAVAILABLE", "unavailable"


    provider = models.CharField(
        max_length=255, 
    )

    provider_plan_id = models.CharField(
        max_length=255
    ) 

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    validity = models.IntegerField()

    duration_category = models.CharField(
        max_length=255
    )

    plan_type_category = models.CharField(
        max_length=255
    )

    availability = models.CharField(
        max_length=50,
        choices=ProductState.choices,
        default=ProductState.AVAILABLE
    )

    supplier_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    margin = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
