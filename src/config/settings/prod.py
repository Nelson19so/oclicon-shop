from .base import *
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

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
        # 'OPTIONS': {'sslmode': 'require'},
        # 'CONN_MAX_AGE': 600,
    }
}

cloudinary.config(
    cloud_name=os.getenv('CLOUD_NAME'),
    api_key=os.getenv('CLOUD_API_KEY'),
    api_secret=os.getenv('CLOUD_API_SECRET'),
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUD_API_KEY'),
    'API_SECRET': os.getenv('CLOUD_API_SECRET'),
}

# Use Cloudinary for media uploads
# MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- STATIC ---
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- ALLOWED HOSTS ---
ALLOWED_HOSTS = ['oclicon-shop.onrender.com']

