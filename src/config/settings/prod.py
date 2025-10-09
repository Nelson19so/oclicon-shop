from .base import *

DEBUG = False 

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

# === Storage ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME")

# Use custom Supabase storage backend
DEFAULT_FILE_STORAGE = "src.apps.common.storage_backends.SupabaseStorage"

# Construct media URL dynamically from Supabase env
MEDIA_URL = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET_NAME}/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Static files (use WhiteNoise)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# allowed host
ALLOWED_HOSTS = ["oclicon-shop.onrender.com"]

"""
Prod.py file is the main oclicon ecommerce website settings conf for live and rea time operation
this is the main ecommerce setup for ready to use
"""
