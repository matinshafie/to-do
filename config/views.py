from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data.get("access")
            refresh = response.data.get("refresh")

            response.set_cookie(
                key="access",
                value=access,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path="/",
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=True,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )
            response.set_cookie(
                key="refresh",
                value=refresh,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path="/",
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=True,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )

            # don't leak tokens in the body
            del response.data["access"]
            del response.data["refresh"]

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh")
        if refresh is None:
            return Response({"detail": "Refresh token not found"}, status=401)

        # inject cookie value into request data so the serializer sees it
        request.data["refresh"] = refresh
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data.get("access")
            response.set_cookie(
                key="access",
                value=access,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path="/",
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=True,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )
            del response.data["access"]

            # rotate refresh token if ROTATE_REFRESH_TOKENS is True
            if response.data.get("refresh"):
                response.set_cookie(
                    key="refresh",
                    value=response.data["refresh"],
                    max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                    path="/",
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=True,
                    samesite=settings.AUTH_COOKIE_SAMESITE,
                )
                del response.data["refresh"]

        return response
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.COOKIES.get("refresh")
        response = Response(status=204)

        if refresh:
            try:
                token = RefreshToken(refresh)
                token.blacklist()  # requires rest_framework_simplejwt.token_blacklist in INSTALLED_APPS
            except Exception:
                pass

        response.delete_cookie("access", path="/")
        response.delete_cookie("refresh", path="/")
        return response