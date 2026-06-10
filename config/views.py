from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request: Request, response: Response, *args, **kwargs):
        if response.data.get('refresh'):
            response.set_cookie(
                key='refresh_token',
                value=response.data['refresh'],
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            del response.data['refresh']
        if response.data.get('access'):
            response.set_cookie(
                key='access_token',
                value=response.data['access'],
                httponly=True,
                secure=True,
                samesite='Lax'
            )
            del response.data['access']

        return super().finalize_response(request, response, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request: Request):
        # 1. Attempt to blacklist the refresh token if using the blacklist app
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass 

        # 2. Create response and clear cookies
        response = Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response