from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .token_service import decode_token, InvalidTokenError
import logging
import jwt


logger = logging.getLogger(__name__)
class JWTAuthentication:

    def authenticate(self, request):
        User = get_user_model()

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):

            _, token = auth_header.split(" ", 1)
        else :
            token = None
        

        if not token:
            return None

        try:
            payload = decode_token(token, "access")

            user = User.objects.get(id=payload["user_id"])

            if not user.is_active:
                logger.warning(f"request receive from inactive user: {user.id}")
                raise AuthenticationFailed("Authentication failed.")

            return (user, token)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Authentication failed.")

        except (jwt.InvalidTokenError, InvalidTokenError):
            raise AuthenticationFailed("Authentication failed.")

        except User.DoesNotExist:
            raise AuthenticationFailed("Authentication failed.")