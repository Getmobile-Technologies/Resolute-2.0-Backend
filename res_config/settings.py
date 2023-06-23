"""
Django settings for res_config project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from django.utils.timezone import timedelta
import dj_database_url
import os
import firebase_admin
from firebase_admin import credentials
import json
import logging


load_dotenv(find_dotenv())


ENVIRONMENT=os.getenv("ENVIRONMENT", "Development")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!


if ENVIRONMENT.title() == "Development":
    
    ALLOWED_HOSTS = []
    DEBUG = True
    DATABASES = {
        'default' : {
            'ENGINE' : 'django.db.backends.sqlite3',
            'NAME' : BASE_DIR/ 'db.sqlite3'
        }
    }
    
    
else:
    
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(',')
    DEBUG = False
    
    CORS_ALLOW_ALL_ORIGIN = True
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_CREDENTIALS = True
    
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config()
    
    # Configure the logging settings
    LOG_DIR = os.path.join(BASE_DIR, 'logs')

    # Ensure the logs directory exists
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Logging configuration for errors
    LOG_FILE_ERROR = os.path.join(LOG_DIR, 'error.log')
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=LOG_FILE_ERROR,
                        filemode='a')

    # Logging configuration for server prints
    LOG_FILE_SERVER = os.path.join(LOG_DIR, 'server.log')
    server_logger = logging.getLogger('django.server')
    server_logger.setLevel(logging.DEBUG)
    server_handler = logging.FileHandler(LOG_FILE_SERVER)
    server_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    server_handler.setFormatter(server_formatter)
    server_logger.addHandler(server_handler)
    
    
    SESSION_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_HOST = None
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER =(
        ('HTTP_X_FORWARDED_PROTO', 'https')
    )
    CSRF_COOKIE_SECURE=False
    
    


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'phonenumber_field',
    'corsheaders',
    'cloudinary',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
    'accounts',
    'main',
    'drf_yasg',
    'coreapi',
    'channels',
    'broadcast',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'res_config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI_APPLICATION = 'res_config.wsgi.application'
ASGI_APPLICATION = 'res_config.asgi.application'

CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
            "CONFIG": {
                # "hosts": [(os.getenv("REDIS_HOST"), int(os.getenv("REDIS_PORT")))],
                # "hosts": [f"redis://{os.getenv('REDIS_HOST')}:{int(os.getenv('REDIS_PORT'))}"],
                "hosts": [os.getenv('REDIS_TLS_URL')],
                
            },
        },
    }

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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



# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



AUTH_USER_MODEL = 'accounts.User'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'UPDATE_LAST_LOGIN': True,
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'BLACKLIST_AFTER_ROTATION': True,
}





REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ['rest_framework_simplejwt.authentication.JWTAuthentication'],
}


AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'django.contrib.auth.backends.AllowAllUsersModelBackend',
        'accounts.authentication.EmailBackend',
        'accounts.authentication.PhoneNumberBackend'

    ]


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv("CLOUD_NAME"),
    'API_KEY': os.getenv("CLOUD_API_KEY"),
    'API_SECRET': os.getenv("CLOUD_API_SECRET")
}

SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
            }
            }
        }

FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
    
cred = credentials.Certificate(json.loads(FIREBASE_CREDENTIALS))

firebase_admin.initialize_app(cred)