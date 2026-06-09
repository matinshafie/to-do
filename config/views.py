from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.request import Request


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