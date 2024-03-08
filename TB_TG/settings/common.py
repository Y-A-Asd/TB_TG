"""
Django settings for TB_TG project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import logging
import os
from pathlib import Path
from celery.schedules import crontab
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
import django
from django.utils.translation import gettext
from django.conf.global_settings import CACHES

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djoser',
    'drf_yasg',
    "compressor",
    'solo',
    'silk',
    'parler',
    "debug_toolbar",
    'django_filters',
    'rest_framework',
    'channels',
    'corsheaders',
    'rosetta',
    'blog',
    'front',
    'discount',
    'core',
    'chat',
    'shop',
    'tags',
]

"""https://tech.raturi.in/compress-and-minify-files-django"""

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',  # This one
    'htmlmin.middleware.HtmlMinifyMiddleware',  # This one
    'htmlmin.middleware.MarkRequestMiddleware',  # This one
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'TB_TG.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TB_TG.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'core.User'
AUTHENTICATION_BACKENDS = ['core.backends.PhoneBackend']

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('fa', _('Persian')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True
USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# COMPRESS_ENABLED = True
COMPRESS_CSS_HASHING_METHOD = 'content'
"""https://django-compressor.readthedocs.io/en/stable/settings.html"""
COMPRESS_CACHE_BACKEND = 'memcache'
COMPRESS_FILTERS = {
    'css': [
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.rCSSMinFilter',
    ],
    'js': [
        'compressor.filters.jsmin.JSMinFilter',
    ]
}
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = True

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'front/static'),
    os.path.join(BASE_DIR, 'shop/static'),
]
"python manage.py collectstatic"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'djmailyosof@gmail.com'
EMAIL_HOST_PASSWORD = 'wlbqpqetjidxlxvs'  # todo : put in dotenv

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'shop.pagination.DefaultPagination',
    # 'PAGE_SIZE': 10,

}

# my config for otp

REDIS_PORT = 6379
REDIS_DB = 2
OTP_EXPIRY_SECONDS = 300

"""
redis commands:
    redis-cli -h localhost -p 6379 -n 2 
    KEYS *
    GET <KEY>
"""

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=3)
}

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserCreateSerializer'
    },
}

PARLER_LANGUAGES = {
    None: (
        {'code': 'en'},
        {'code': 'fa'},
    ),
    'default': {
        'fallback': 'en',
        'hide_untranslated': False,
    }
}
CELERY_IMPORTS = (
    'core.tasks',
)

CELERY_BEAT_SCHEDULE = {
    'delete_inactive_users': {
        'task': 'core.tasks.delete_inactive_users',
        'schedule': timedelta(hours=24),
    },
    'send_promotion_emails': {
        'task': 'core.tasks.send_promotion_emails',
        'schedule': timedelta(hours=24),
    },
    'send_birthday_emails': {
        'task': 'core.tasks.send_birthday_emails',
        'schedule': timedelta(hours=24),
    },
    'delete_old_carts': {
        'task': 'core.tasks.delete_old_carts',
        'schedule': crontab(hour='*/24'),
    },
}
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

"""
celery command:
    celery -A TB_TG beat -> apply beat worker
    celery -A TB_TG flower -> apply flower celery manager at localhost:5555
    celery -A TB_TG worker --loglevel=info -> run celery worker
    

"""

"""
    sudo systemctl start memcached
"""

"""
how to use cache in class base views:
    @method_decorator(cache_page(60) -> 1 minute cache
"""

LOGGING = {
    'version': 1.0,
    'disable_existing_loggers': False,
    'handlers': {
        'security': {
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'verbose',
            'level': 'INFO',
        },
        'views': {
            'class': 'logging.FileHandler',
            'filename': 'logall.log',
            'formatter': 'verbose',
            'level': 'INFO',
        }
    },
    'loggers': {
        'security_logger': {
            'handlers': ['security'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'views_logger': {
            'handlers': ['views'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': False,
        }
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} %({levelname})s - {name} - {message}',
            'style': '{'
        }
    }
}

CART_SESSION_ID = 'cart'

"""
for run server 
    use this command ->      gunicorn TB_TG.wsgi
"""

"""
feat: (new feature for the user, not a new feature for build script)
fix: (bug fix for the user, not a fix to a build script)
docs: (changes to the documentation)
style: (formatting, missing semi colons, etc; no production code change)
refactor: (refactoring production code, eg. renaming a variable)
test: (adding missing tests, refactoring tests; no production code change)
chore: (updating grunt tasks etc; no production code change)

"""

MERCHANT = "00000000-0000-0220-0000-000000000000"

SANDBOX = True
if SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API = f"https://{sandbox}.zarinpal.com/pg/services/WebGate/wsdl"
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/v4/payment/request.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/v4/payment/verify.json"

CORS_ALLOW_ALL_ORIGINS = True