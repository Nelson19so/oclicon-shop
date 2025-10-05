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
        'OPTION': {
            'sslomode': 'require'
        },
        'CONN_MAX_AGE': 60,
    }
}

# === Storage ===
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = os.getenv("SUPABASE_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("SUPABASE_SECRET_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME")

# Supabase S3 endpoint
AWS_S3_ENDPOINT_URL = os.getenv("SUPABASE_S3_ENDPOINT")
AWS_S3_REGION_NAME = None  # Supabase doesn’t require region
AWS_S3_USE_SSL = True
AWS_S3_VERIFY = True

# Makes URLs public
AWS_QUERYSTRING_AUTH = False

# Optional - custom domain for files
AWS_S3_CUSTOM_DOMAIN = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}"

# Static files (use WhiteNoise)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# allowed host
ALLOWED_HOSTS = ["oclicon-shop.onrender.com"]

"""
Prod.py file is the main oclicon ecommerce website settings conf for live and rea time operation
this is the main ecommerce setup for ready to use
"""
