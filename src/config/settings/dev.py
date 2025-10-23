from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# dev database 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Media files config for development
MEDIA_ROOT = BASE_DIR / 'media' 
MEDIA_URL = '/media/'
