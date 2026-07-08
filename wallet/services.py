from .models import Wallet
import logging
from django.db import transaction
from transactions.models import Transaction
from payments.providers.paystack import initialize_payment
import logging


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


# creating wallet
def create_wallet(user):

    if Wallet.objects.filter(user=user).exists():
        logger.warning(
            "Wallet already exists for user %s",
            user.id
        )
        raise WalletAlreadyExistsError("wallet already exists!")
    
    
    wallet = Wallet.objects.create(
        user=user
    )

    logger.info(
        "Wallet created for user %s",
        user.id
    )

    return wallet

# depositing process one 
def deposit_money(user, amount):

    if amount <= 0:
        logger.critical(
            "Negative Deposit issue %s",
            user.id
        )
        raise InvalidDepositAmountError(
            "Deposit amount must be greater than zero."
        )
    

    wallet=user.wallet
    
    with transaction.atomic():
        deposit_transaction = Transaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=Transaction.Type.DEPOSIT,
        )

        payment = initialize_payment(
            deposit_transaction
        )
        
        
        deposit_transaction.payment_url = payment["payment_url"]
        deposit_transaction.provider_reference = payment["provider_reference"]

        deposit_transaction.save()

        return payment["payment_url"]


        
def complete_deposit(payment_transaction):
    with transaction.atomic(): 
        try: 
            locked_transaction = (
                Transaction.objects
                .select_for_update()
                .get(id=payment_transaction.id)
            )

            wallet = locked_transaction.wallet
            
            if locked_transaction.status == Transaction.Status.SUCCESS:
                logger.warning(
                    "completed transaction happen by %s",
                    locked_transaction.wallet.user.id
                )
                raise DepositAlreadyCompletedError("Transaction succeed Error.")
            
            wallet.balance += locked_transaction.amount
            
            locked_transaction.status = Transaction.Status.SUCCESS

            wallet.save()
            locked_transaction.save()

            return locked_transaction

            
        except Transaction.DoesNotExist:
            raise DepositNotFound("Traction Not Found Error.")
        


