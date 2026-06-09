from django.urls import path, include
from .views import CookieTokenObtainPairView


urlpatterns = [
    path('jwt/create', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]