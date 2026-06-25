from django.utils import timezone
from datetime import timedelta
import jwt 
from django.conf import settings
import logging
from . models import User
logger = logging.getLogger(__name__)

class AuthError(Exception):
    pass

class InvalidTokenError(AuthError):
    pass


    
# generating email  jwt token  using PYJWT
def generate_email_verification_token(user):
    expiration = timezone.now()  + timedelta(hours=settings.EMAIL_VERIFICATION_TOKEN_LIFETIME_HOURS)  

    secret_key = settings.SECRET_KEY
    payload = {
        "user_id": user.id,
        "purpose": "email_verification",
        "exp": expiration,
    }
    jwt_string = jwt.encode(
        payload,
        secret_key,
        algorithm="HS256"
    )

    return jwt_string


# generate access token 
def generate_access_token(user):
    expiration = timezone.now() + timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME_MINUTES)


    payload = {
        "user_id":user.id,
        "purpose":"access",
        "exp":expiration
    }


    jwt_string = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return jwt_string


# generate refresh token 
def generate_refresh_token(user):
    expiration = timezone.now() + timedelta(days=settings.REFRESH_TOKEN_LIFETIME_DAYS)


    payload = {
        "user_id":user.id,
        "purpose":"refresh",
        "exp":expiration
    }

    jwt_string = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return jwt_string







# decoding JWT token

def decode_token(token, purpose):
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )

    if payload.get("purpose") != purpose:
        logger.warning( 
                "Invalid token purpose"
            )
        raise InvalidTokenError("Invalid token purpose")

    return payload
    

# verifying jwt token
def verify_email_verification_token(token):


    try:

        payload = decode_token(
            token, 
            "email_verification"
        )
        
        user = User.objects.get(
            id=payload.get("user_id")
        )

        if user.email_verified: 
            return user

        user.email_verified = True
        user.save(update_fields=["email_verified"])

        logger.info(
            f"User {user.id} verified email"
        )

        return user
    

    except jwt.ExpiredSignatureError:
        logger.warning(
            "Expired verification token"
        )
        raise InvalidTokenError("Invalid token")

    except jwt.InvalidTokenError:
        logger.warning(
            "Invalid verification token"
        )
        raise InvalidTokenError("Invalid verification token")

    except User.DoesNotExist:
        logger.warning(
            "Verification token references missing user"
        )
        raise InvalidTokenError()



def verify_refresh_token(token):
    try : 

        payload = decode_token(
            token,
           "refresh" 
        )    

        user = User.objects.get(
            id=payload.get("user_id")
        )

        if not user.is_active or not user.email_verified:
            raise InvalidTokenError("Invalid refresh token error")
        

        return user


    except jwt.ExpiredSignatureError:
        logger.warning(
            "Expired refresh token"
        )
        raise InvalidTokenError("Invalid token")

    except jwt.InvalidTokenError:
        logger.warning ("Invalid refresh token")
        raise InvalidTokenError("Invalid refresh token error")
    

    except User.DoesNotExist:
        logger.warning(
            "User not found"
        )

        raise InvalidTokenError()
    


def refresh_access_token(token):
    user = verify_refresh_token(
        token
    )

    access_token = generate_access_token(
        user
    )

    return {
        "access_token": access_token 
    }

