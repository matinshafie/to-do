from django.urls import path, include
from .views import CookieTokenObtainPairView, CookieTokenRefreshView

urlpatterns = [
    path("jwt/create/", CookieTokenObtainPairView.as_view()),
    path("jwt/refresh/", CookieTokenRefreshView.as_view()),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
]