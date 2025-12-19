from .base import *
# 
import cloudinary
import cloudinary.uploader
import cloudinary.api
# 

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# dev database 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Media files config for development
# MEDIA_ROOT = BASE_DIR / 'media' 
# MEDIA_URL = '/media/'
