from .base import *
import os

DEBUG = False 

# --- DATABASE CONFIGURATION ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {'sslmode': 'require'},
        'CONN_MAX_AGE': 600,
    }
}

# --- CLOUDINARY CONFIGURATION ---
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')

# Use Cloudinary for media uploads
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- MEDIA & STATIC ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' 

# --- ALLOWED HOSTS ---
ALLOWED_HOSTS = ['oclicon-shop.onrender.com']

"""
This prod.py config connects Django media uploads to Cloudinary CDN for production.
Uploaded images will appear in your Cloudinary dashboard automatically.
"""
