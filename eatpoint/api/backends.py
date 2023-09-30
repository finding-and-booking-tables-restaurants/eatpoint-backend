import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from users.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    www_authenticate_realm = "api"
    authentication_header_prefix = "Bearer"

    def authenticate(self, request, token=None):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header or len(auth_header) != 2:
            return None

        prefix, token = (
            auth_header[0].decode("utf-8").lower(),
            auth_header[1].decode("utf-8"),
        )

        if prefix != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def authenticate_header(self, request):
        return f"Basic realm={self.www_authenticate_realm}"

    @staticmethod
    def _authenticate_credentials(request, token):
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256"
            )
        except exceptions.AuthenticationFailed:
            msg = "Ошибка аутентификации. Невозможно декодировать токен."
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload["user_id"])
        except User.DoesNotExist:
            msg = "No user matching this token was found."
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "Данный пользователь не активирован."
            raise exceptions.AuthenticationFailed(msg)

        return user, token
