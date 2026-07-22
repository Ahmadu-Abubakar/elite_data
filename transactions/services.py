from .models import Transaction


def get_transaction_history(user):
    return (
        Transaction.objects
        .filter(wallet=user.wallet)
        .order_by("-created_at")
    )
