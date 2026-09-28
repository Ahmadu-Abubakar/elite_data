from django.db import models


class Metrics(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    recorded_at = models.DateTimeField(auto_now_add=True)



class Alert(models.Model):
    class Type(models.TextChoices):
        PROVIDER_CONTRACT_CHANGED = "PROVIDER_CONTRACT_CHANGED", "Provider contract changed"
        DATABASE_UNAVAILABLE = "DATABASE_UNAVAILABLE", "Database unavailable"
        SUSPICIOUS_ACTIVITY = "SUSPICIOUS_ACTIVITY", "Suspicious activity"
        PROVIDER_RESPONSE_UNEXPECTED = "PROVIDER_RESPONSE_UNEXPECTED", "provider response unexpected"


    class Severity(models.TextChoices):
        CRITICAL = "CRITICAL", "critical"
        WARNING = "WARNING", "warning"

    class Status(models.TextChoices):
        OPEN = "OPEN", "open"
        RESOLVED = "RESOLVED", "resolved"

    alert_type = models.CharField(
        max_length=50,
        choices=Type.choices
    )

    description = models.CharField(max_length=255)
    severity = models.CharField(
        max_length=30,
        choices=Severity.choices,
        default=Severity.WARNING
    )
    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.OPEN
    )
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)


# Create your models here.
