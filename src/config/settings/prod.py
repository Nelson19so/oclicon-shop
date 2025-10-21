from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'sslmode': 'require'
        },
        'CONN_MAX_AGE': 600,
    }
}

DEFAULT_FILE_STORAGE = "src.apps.common.storage_backends.BytescaleStorage"

MEDIA_URL = "https://upcdn.io/"  # optional, just a reference
MEDIA_ROOT = ""  # not used for Bytescale

# Static files (using WhiteNoise)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Allowed host
ALLOWED_HOSTS = ["oclicon-shop.onrender.com"]

"""
Prod.py file is the main oclicon ecommerce website settings conf for live and rea time operation
this is the main ecommerce setup for ready to use
"""
