from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .token_service import decode_token


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

            return (user, token)

        except User.DoesNotExist:
            raise AuthenticationFailed("User not Found!.")

    