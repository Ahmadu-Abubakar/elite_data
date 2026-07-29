from .models import Wallet
import logging
from django.db import transaction
import logging
from payments.fake_bank import FakeBankProvider
from wallet.models import Wallet
from transactions.models import Transaction


logger = logging.getLogger(__name__)


class WalletException(Exception):
    """Base Exception for all wallet issues"""
    pass

class WalletAlreadyExistsError(WalletException):
    """Raised when wallet already exist"""
    pass

class InvalidDepositAmountError(WalletException):
    """negative deposit valueError"""
    pass

class DepositAlreadyCompletedError(WalletException):
    """Transaction status already succeeded"""
    pass

class DepositNotFound(WalletException):
    """Transaction id not found"""
    pass

class VirtualAccountError(WalletException):
    """Account Not Found!"""
    pass



# creating wallet
def create_wallet(user):

    if Wallet.objects.filter(user=user).exists():
        logger.warning(
            "Wallet already exists for user %s",
            user.id
        )
        raise WalletAlreadyExistsError("wallet already exists!")
    
    
    account = FakeBankProvider.create_virtual_account(user)

    wallet = Wallet.objects.create(
        user=user,
        account_number=account["account_number"],
        account_name=account["account_name"],
        bank_name=account["bank_name"],
        provider_reference=account["provider_reference"],

    )

    logger.info(
        "Wallet created for user %s",
        user.id
    )

    return wallet



def handle_deposit_webhook(payload):
    return record_processed_deposit(payload)

def validate_deposit(payload):

    # wallet lookup 
    try :
        wallet = Wallet.objects.get(
            account_number=payload["account_number"]
        )
    except Wallet.DoesNotExist:
        raise VirtualAccountError("Invalid user account")

    
    found_provider = Transaction.objects.filter(
        provider_reference=payload["provider_reference"]
    ).exists()


    if payload["amount"] <= 0:
        raise InvalidDepositAmountError("Invalid Balance!.")


    if found_provider:
        raise VirtualAccountError("Transaction has been made successfully!!. ")

    if payload['status'].lower() != "success":
        raise VirtualAccountError("Invalid Deposit Error !.")


    return (wallet, payload)



def credit_wallet(wallet, amount):
    wallet.balance += amount
    wallet.save()
    return wallet

def create_transaction(wallet, payload):
    
    transaction =Transaction.objects.create(
        wallet=wallet,
        amount=payload['amount'],
        status=Transaction.Status.SUCCESS,
        transaction_type=Transaction.Type.DEPOSIT,
        provider_reference=payload['provider_reference'],
        description=f"₦{payload['amount']} - Deposit " 
    )
    return transaction


def record_processed_deposit(payload):

    # validation 
    wallet, payload = validate_deposit(payload)

    with transaction.atomic():
        amount = payload['amount']
        wallet = credit_wallet(wallet, amount)
        create_transaction(wallet, payload)

        return {
            "message" : "SUCCESS"
        }

