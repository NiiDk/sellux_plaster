import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-sellux-plaster-key-123')

# Check if running on Render
IS_RENDER = os.getenv('RENDER', 'False') == 'true'

# Smart DEBUG setting
if IS_RENDER:
    DEBUG = os.getenv('DEBUG', 'False') == 'True'
else:
    DEBUG = True

# Smart ALLOWED_HOSTS
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'sellux-plaster.onrender.com']
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Additional wildcard for safety locally
if not IS_RENDER:
    ALLOWED_HOSTS.append('*')

# CSRF Trusted Origins for Render (Required for HTTPS)
CSRF_TRUSTED_ORIGINS = ['https://sellux-plaster.onrender.com']
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third Party
    'cloudinary_storage',
    'cloudinary',
    'crispy_forms',
    'crispy_bootstrap5',

    # Local Apps
    'accounts',
    'pages',
    'portfolio',
    'catalogue',
    'orders',
    'faq',
    'contact',
    'dashboard',
    'custom_requests',
    'services',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Safe to keep for both
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sellux_plaster.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sellux_plaster.wsgi.application'

# Smart Database configuration
if IS_RENDER:
    # Production: Use PostgreSQL from DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    # Local: Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (Whitenoise)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Smart Storages (Media & Static)
if IS_RENDER:
    # Production: Cloudinary for Media, Whitenoise for Static
    STORAGES = {
        "default": {
            "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
else:
    # Local: FileSystem for Media, Standard for Static
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }

# Cloudinary configuration (Always loaded, but only used via STORAGES on Render)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dkvcn0j3c',
    'API_KEY': '631397258551635',
    'API_SECRET': '3baovFkOnDRs1eLnZpOLNv4RXR4',
}

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Paystack Config
PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY')
CURRENCY_CODE = os.getenv('CURRENCY_CODE', 'GHS')

# Login/Logout redirects
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'pages:home'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
