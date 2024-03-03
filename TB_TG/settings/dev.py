from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^r6+$o=0!juwr_0k89v86z93ikk&3=f1#fdxrse&k52vi*7e_u'

if DEBUG:
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tb_tg',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
