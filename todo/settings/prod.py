from .base import *  # noqa: F401,F403
from os import getenv

DEBUG = False

ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

INSTALLED_APPS += [
    'corsheaders',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': getenv('MYSQL_DATABASE'),
        'USER': getenv('MYSQL_USER'),
        'HOST': getenv('MYSQL_HOST'),
        'PASSWORD': getenv('MYSQL_PASSWORD'),
        'CONN_MAX_AGE': 60,
    }
}

CORS_ALLOWED_ORIGINS = getenv('CORS_ALLOWED_ORIGINS', '').split(',')

# --- Security hardening ---
AUTH_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_CONTENT_TYPE_NOSNIFF = True

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Logs to stdout so Docker/Gunicorn/systemd can capture them
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}