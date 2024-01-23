from .common import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['']
SECRET_KEY = os.environ['SECRET_KEY']
