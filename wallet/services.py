from .models import Wallet
import logging


logger = logging.getLogger(__name__)


class WalletException(Exception):
    """Base Exception for all wallet issues"""
    pass

class WalletAlreadyExistsError(WalletException):
    """Raised when wallet already exist"""
    pass



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
