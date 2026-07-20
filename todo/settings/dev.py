from .base import *  # noqa: F401,F403
from os import getenv

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS += [
    'debug_toolbar',
    'drf_spectacular_sidecar',
    'corsheaders',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
]

SPECTACULAR_SETTINGS = {
    **SPECTACULAR_SETTINGS,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': getenv('MYSQL_DATABASE'),
        'USER': getenv('MYSQL_USER'),
        'HOST': getenv('MYSQL_HOST'),
        'PASSWORD': getenv('MYSQL_ROOT_PASSWORD'),
    }
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

# Not HTTPS locally, so cookies can't be marked secure
AUTH_COOKIE_SECURE = False