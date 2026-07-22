from .models import Transaction
from rest_framework import serializers

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "reference",
            "status",
            "amount",
            "telecom_providers",
            "description",
            "transaction_type",
            "created_at"
        ]