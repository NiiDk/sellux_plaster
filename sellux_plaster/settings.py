import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# 1. Load the .env file immediately
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Security Settings
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-sellux-plaster-key-123')

# We check the .env file. If DEBUG is not there, default to False (Production mode).
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# 3. ALLOWED HOSTS (Fixed the missing quote here)
ALLOWED_HOSTS = ['178.128.40.175', 'selluxplaster.com', 'localhost', '127.0.0.1']

# CSRF Trusted Origins (Vital for forms to work on the live site)
CSRF_TRUSTED_ORIGINS = ['https://selluxplaster.com', 'http://178.128.40.175']

# 4. Production Security Headers (Active when DEBUG is False)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # HSTS settings (Uncomment these once you have HTTPS/SSL set up later)
    # SECURE_SSL_REDIRECT = True
    # SECURE_HSTS_SECONDS = 31536000
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    # Third Party Apps
    'cloudinary_storage',
    'cloudinary',
    'mathfilters',
    'crispy_forms',
    'django.contrib.humanize',
    'crispy_bootstrap5',
    'axes',  # Brute force protection

    # Local Apps
    'core',
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
    'cart',
    'estimation',
    'shipping',
    'promotions',
    'about',
    'team',
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Vital for CSS on DigitalOcean
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
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
                'core.context_processors.brand_context',
                'core.context_processors.cart_context',
                'core.context_processors.promotions_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'sellux_plaster.wsgi.application'

# 5. Database Configuration
# This looks for DATABASE_URL in .env (Postgres). If not found, uses SQLite.
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600
    )
}

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 6. Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 7. Storage Configuration (Cloudinary for Media, WhiteNoise for Static)
# This ensures images work on DigitalOcean without needing "Render" variables.
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME', 'dkvcn0j3c'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY', '631397258551635'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET', '3baovFkOnDRs1eLnZpOLNv4RXR4'),
}

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Paystack configuration
PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY', '')
PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY', '')
CURRENCY_CODE = 'GHS'
CURRENCY_SYMBOL = 'GH₵'

# Cart configuration
CART_SESSION_ID = 'cart'

# Axes configuration
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_LOCK_OUT_AT_FAILURE = True

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Login/Logout URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'pages:home'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {'console': {'class': 'logging.StreamHandler'}},
        'root': {'handlers': ['console'], 'level': 'DEBUG'},
    }
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {'console': {'class': 'logging.StreamHandler'}},
        'root': {'handlers': ['console'], 'level': 'ERROR'},
    }