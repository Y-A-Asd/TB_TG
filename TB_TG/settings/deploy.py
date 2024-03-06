from .common import *
import os
DEBUG = True
# SECURITY WARNING: don't run with debug turned on in production!
SECRET_KEY = os.environ['SECRET_KEY']

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tb_tg',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

REDIS_HOST_OTP = 'redis'

CELERY_BROKER_URL = 'redis://redis:6379/1'

CACHES['memcache'] = {

    "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
    "LOCATION": "memcached:11211",
}
