import secrets
import string
import hmac
import hashlib

import time

import os
from .models import OTP
from notifications.emails import send_email
from django.db import transaction


from django.core.exceptions import ValidationError
# Otp exceptions handler
class OtpException(Exception):
    """Raised when otp issue happens!."""
    pass
class MissingKeyError(OtpException):
    """Raised when key is missing!. """
    pass

class EmailDeliveryError(OtpException):
    """Raised when the email delivery fails"""
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

# Store Otp to postgres and send that otp through email
def store_and_deliver_otp(user, purpose):
    otp_payload = digest_otp(user)

    
    # old challenge
    older_challenge = OTP.objects.filter(
        user=otp_payload["user"],
        purpose=purpose,
        status=OTP.Status.ACTIVE
    )

    # creating new challenge
    otp_challenge = OTP.objects.create(
        user=otp_payload["user"],
        email=otp_payload["email"],
        purpose=purpose,
        otp_hash=otp_payload["keyed_otp"],
        expired_at=otp_payload["expired_at"]
    )



    try:
        send_email(
            recipient=otp_payload["email"],
            subject="Verify your email address — Elite Data",
            body=f"""
                Hi,

                Welcome to Elite Data!

                Use the verification code below to verify your email address:
                
                {otp_payload["otp_code"]}

                This code expires in 2 minutes. For your security, do not share it with anyone.

                If you didn't request this code, you can safely ignore this email.

                Thank you,

                The Elite Data Team
            """
        )

        # commit the challenges state in one data base transaction 
        with transaction.atomic():

            # terminate the old challenge
            if older_challenge.exists():
                older_challenge.update(status=OTP.Status.INVALIDATED)
        
            # Active the new born challenge
            otp_challenge.status=OTP.Status.ACTIVE
            otp_challenge.save(update_fields=['status'])


    except EmailDeliveryError as e:

        otp_challenge.status=OTP.Status.INVALIDATED
        otp_challenge.save(update_fields=["status"])

        raise ValidationError(f"email delivery failed: {str(e)}")
    return True




# otp verification process 
def verify_otp_challenge(user, otp_code):
    pass
