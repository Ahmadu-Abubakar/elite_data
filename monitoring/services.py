from .models import Metrics, Alert
from decimal import Decimal
from django.utils import timezone

class Monitoring:

    @staticmethod
    def metric(name:str, value : int | Decimal):
        Metrics.objects.create(
            name=name,
            value=value
        )

    @staticmethod
    def alert(
        alert_type : Alert.Type,
        description : str,
        severity : Alert.Severity = Alert.Severity.WARNING
    ):


        Alert.objects.create(
            alert_type=alert_type,
            description=description,
            severity=severity
        )


    @staticmethod
    def resolve_alert(alert_id):
        alert = Alert.objects.get(id=alert_id)

        if alert.status != Alert.Status.OPEN:
            return

        alert.status = Alert.Status.RESOLVED
        alert.resolved_at = timezone.now()

        return alert.save()



