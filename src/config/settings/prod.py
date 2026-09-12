from .base import *
import os
import cloudinary
import dj_database_url

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key-for-vercel-building')

DEBUG = False 

# db_from_env = dj_database_url.config(conn_max_age=600)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres.dyh5dzke6',
        'PASSWORD': 'k@UM?*s.X*64/hY',
        'HOST': 'db.hqrjqvpogizggxmttopx.supabase.co',
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},
        # 'CONN_MAX_AGE': 600,
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': 'localhost',
#         'PORT': '5432',
#         # 'OPTIONS': {'sslmode': 'require'},
#         # 'CONN_MAX_AGE': 600,
#     }
# }


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

# STATIC
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ALLOWED HOSTS
ALLOWED_HOSTS = ['oclicon-shop.onrender.com', '.vercel.app', 'now.sh', 'localhost', '127.0.0.1']

