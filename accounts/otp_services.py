import secrets
import string
import hmac
import hashlib

import time

import os
from .models import OTP


# Otp exceptions handler
class OtpException(Exception):
    """Raised when otp issue happens!."""
    pass
class MissingKeyError(OtpException):
    """Raised when key is missing!. """
    pass

def generate_otp():
    otp_digits = string.digits

    otp_code = ''.join(secrets.choice(otp_digits) for _ in range(6))


    return otp_code
        


def digest_otp(user):

    otp_code = generate_otp()

    # expiry time
    expired_at = int(time.time()) + 120


    # hmac message 
    message = f"{user.id}:{otp_code}:{expired_at}".encode("utf-8")


    raw_key = os.getenv('HMAC_SECRET_KEY')

    if not raw_key:
        raise MissingKeyError("missing HMAC key!. ")  

    secret_byte_key = raw_key.encode('utf-8')


    keyed_otp = hmac.digest(secret_byte_key, message, hashlib.sha256)

    result = {
        "user" : user,
        "keyed_otp" : keyed_otp,
        "email" : user.email,
        "otp_code" : otp_code, 
        "expired_at" : expired_at
    }

    return result

# Store Otp to postgres
def store_otp(user, purpose):
    otp_payload = digest_otp(user)
    OTP.objects.create(
        user=otp_payload["user"],
        email=otp_payload["email"],
        purpose=purpose,
        otp_hash=otp_payload["keyed_otp"],
        expired_at=otp_payload["expired_at"]
    )

    return otp_payload["otp_code"], otp_payload["email"]

