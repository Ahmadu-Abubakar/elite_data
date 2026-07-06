import requests
from django.conf import settings
from payments.exceptions import (
    PaymentInitializationError,
    PaymentVerificationError
)
from transactions.models import Transaction
import logging


logger = logging.getLogger(__name__)




def initialize_payment(transaction):

    url = f"{settings.PAYSTACK_BASE_URL}/transaction/initialize"

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    payload = {
        "email": transaction.wallet.user.email,
        "amount": int(transaction.amount * 100),
        "reference": str(transaction.reference),
    }



    try:
        
        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            timeout=30,
        )

        response.raise_for_status()

    except requests.Timeout:
        raise PaymentInitializationError(
            "Payment provider timed out."
        )

    except requests.RequestException:
        raise PaymentInitializationError(
            "Unable to initialize payment."
        )


    data = response.json()["data"]

    return {
        "payment_url": data["authorization_url"],
        "provider_reference": data["reference"],
    }


def verify_payment(reference): 

    try:
        transaction = Transaction.objects.get(reference=reference)
        url =  f"{settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}"

    except Transaction.DoesNotExist:
        raise PaymentVerificationError(
            "Invalid reference"
        )



    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    
    try:
        response = requests.get(
            url=url,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()


    except requests.Timeout:
        raise PaymentVerificationError(
        "Payment verification timed out."
    )
    
    except requests.RequestException as e:
        raise PaymentVerificationError(
            "Invalid verification request."
        )from e
    
    data = response.json()["data"]
    
    if data["currency"] != settings.DEFAULT_CURRENCY:
        raise PaymentVerificationError(
            "Invalid currency Type."
        )
    
    expected_amount = int(transaction.amount * 100)

    if data["amount"] != expected_amount:
        raise PaymentVerificationError(
            "Invalid transaction."
        )


    if data["status"] == "success":
        return {
            "verified": True,
            "amount" : data["amount"],
            "provider_reference" : data["reference"]
        }

    return {
        "verified": False
    }


