from .base import *

DEBUG = False

# allowed url
ALLOWED_HOSTS = ["oclicon-shop.onrender.com"]

# dev database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

"""
Staging.py file is a demo preview of oclicon ecommerce website
this is different from prod and it is for testing the website for recommendations

in .env set 'config.settings.staging' to be able to use it for testing
"""