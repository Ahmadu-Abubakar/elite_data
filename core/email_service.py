# send email infrastructure 
# core/email_service.py

import logging

from django.conf import settings
from django.core.mail import send_mail


logger = logging.getLogger(__name__)


def send_email(
    *,
    recipient: str,
    subject: str,
    body: str,
) -> None:

    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=False,
        )

    except Exception:
        logger.exception(
            "Failed to send email to %s",
            recipient,
        )
        raise