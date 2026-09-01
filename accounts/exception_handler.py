
# custom exception_handler 
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    if isinstance(exc, ValidationError):
        response.data = {
            "success": False,
            "message": "Validation failed.",
            "errors": response.data,
        }

    return response






# Custom Exception___________
class AuthError(Exception):
    """Base exception for all authentication and authorization issues."""
    pass

class InvalidCredentialsError(AuthError):
    """Raised when the provided username or password is incorrect."""
    pass

class EmailNotVerifiedError(AuthError):
    def __init__(self, message="Email address has not been verified.", email=None):
        super().__init__(message)
        self.email = email 




