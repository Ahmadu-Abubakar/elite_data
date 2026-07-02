

class PaymentError(Exception):
    """Base payment exceptions."""
    pass

class PaymentProvidersUnreachableError(PaymentError):
    """cannot communicate with providers"""
    pass


class PaymentInitializationError(PaymentError):
    """Provider failed to initialize payment."""
    pass


class PaymentVerificationError(PaymentError):
    """Payment could not be verified."""
    pass