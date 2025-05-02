from dotenv import load_dotenv
from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('django-secret-key')
if SECRET_KEY is None:
    raise ImproperlyConfigured("Please set the SECRET_KEY environment variable")

# SECURITY WARNING: run with debug turned off in production!
DEBUG = True

ALLOWED_HOSTS = [
  "127.0.0.1",
  "localhost",
  "oclicon-shop.onrender.com",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',  # Required for django-allauth
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # installed apps    
    'django',  # Django framework (this is built-in)
    'crispy_forms',  # For Django crispy forms
    'crispy_bootstrap5',  # Bootstrap 5 integration for crispy forms
    'allauth',  # Main authentication framework
    'allauth.account',  # Email/password authentication
    'allauth.socialaccount',  # Social authentication
    'allauth.socialaccount.providers.google',  # Google login
    'allauth.socialaccount.providers.apple',  # Apple login
    
    'apps.accounts', # user account app
    'apps.cart', # cart product app
    'apps.orders', # order product app
    'apps.products', # product app
    'apps.public', # public urls

    # Add your own apps here
]


# debugging toolbar
# INTERNAL_IPS = [
#     "127.0.0.1",
# ]

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Add this before other middleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Must come before AccountMiddleware for allAuth
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
          BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'settings.context_processors.navbar_categories_list', # context for navbar categories
                'settings.context_processors.navbar_cart_display_list', # context for navbar cart_list
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

# whitenoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# postGresSql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),         # Replace with your DB name
        'USER': os.getenv('DB_USER'),        # Replace with your DB username
        'PASSWORD': os.getenv('DB_PASSWORD'),    # Replace with your DB password
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),                 # Default PostgreSQL port
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Email settings (example for using Gmail's SMTP server)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Replace with your email
EMAIL_HOST_PASSWORD = 'your-email-password'  # Replace with your email password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'  # Default sender email

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
  BASE_DIR / 'static'
]

STATIC_ROOT = os.path.join(BASE_DIR / 'staticfiles')

# This only applies in production mode (DEBUG=False)
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# media files/images conf
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# crispy boostrap5 
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

SITE_ID = 1

# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Social Account Providers
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '<your-google-client-id>'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '<your-google-client-secret>'

SOCIAL_AUTH_APPLE_ID_KEY = '<your-apple-client-id>'
SOCIAL_AUTH_APPLE_ID_SECRET = '<your-apple-client-secret>'

# For Allauth configuration
SOCIALACCOUNT_PROVIDERS = {
    # https://console.developers.google.com
    'google': {
        'SCOPE': ['email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
    },

    # https://developer.apple.com/
    'apple': {
        'SCOPE': ['email'],
    },
}

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',  # Default backend
)

# Redirect URLs after login or signup
LOGIN_REDIRECT_URL = '/'  # Redirect after successful login/signup
LOGOUT_REDIRECT_URL = '/'
