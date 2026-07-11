from django.conf import settings
from .models import User
import logging
from core.email_service import send_email
from . token_service import generate_access_token, generate_refresh_token

logger = logging.getLogger(__name__)
    

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

# authenticate user___________

def authenticate_user(email, password):

    try:
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        raise InvalidCredentialsError(
            "Invalid email or password"
        )

    if not user.check_password(password):
        raise InvalidCredentialsError(
            "Invalid email or password"
        )

    if not user.email_verified:
        logger.warning(
            "Login attempt by unverified user: %s",
            user.id
        )

        raise EmailNotVerifiedError(
            email=email
        )
    return user


    

# sending email verification toke____
def send_verification_email(user, token):
    subject = "Verify your EliteData account"

    verification_url = (
        f"http://localhost:8000/api/accounts/verify/{token}/"
    )
    body = (
        "Welcome to EliteData.\n\n"
        "Please verify your email address by visiting:\n\n"
        f"{verification_url}\n\n"
        "If you did not create this account, ignore this email."
    )
        
    print("TOKEN:")
    print(repr(token))

    print("URL:")
    print(repr(verification_url))

    logger.info(
        "Verification URL: %s",
        verification_url
    )
    
    send_email(
        recipient=user.email,
        subject=subject,
        body=body,
    )



# logging-in user____________
def login_user(email, password):
    user = authenticate_user(email, password)

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    return {
        "access_token" : access_token,
        "refresh_token"  : refresh_token,
        "user" : {
            "user_id": user.id,
            "email": user.email,
            "username": user.username
        }
    }


