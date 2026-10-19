from django.db import models
import uuid

class Synchronization(models.Model):
    class Status(models.TextChoices):
        FAILED = "FAILED", "failed"
        RUNNING = "RUNNING", "running"
        SUCCEEDED = "SUCCEEDED", "SUCCEEDED"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.RUNNING
    )

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)



# Create your models here.
