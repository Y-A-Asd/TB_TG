from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0uwk9*8mltebnrrdn(zawxdyh-8b*s6$!0n(lb(cwlk+@otvzq'

if DEBUG:
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

"""for docker"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

CACHES['memcache'] = {

    "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
    "LOCATION": "localhost:11211",
}

REDIS_HOST_OTP = 'localhost'

CELERY_BROKER_URL = 'redis://localhost:6379/4'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('localhost', 6379)],
        },
    },
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

ALLOWED_HOSTS = ["*"]
