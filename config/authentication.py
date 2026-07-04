from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get("access")

        if access_token is None:
            return None  # let other authenticators run, or return anonymous

        try:
            validated_token = self.get_validated_token(access_token)
        except InvalidToken:
            return None

        return self.get_user(validated_token), validated_token