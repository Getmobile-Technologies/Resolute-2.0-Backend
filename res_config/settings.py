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


load_dotenv(find_dotenv())
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("MYKEY")

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = ['resolute.herokuapp.com', '127.0.0.1', '0.0.0.0:$PORT', 'localhost']

CSRF_TRUSTED_ORIGINS = ['https://resolute.herokuapp.com' ,'https://*.127.0.0.1', 'http://localhost']


CORS_ALLOWED_ORIGINS = [
    "http://localhost:4000",
    "http://127.0.0.1:8080",
    "https://resolute.herokuapp.com"

]

CORS_ALLOW_ALL_ORIGIN = True
CORS_ALLOW_HEADERS = [
    'baggage',
    'content-type',
    'authorization',
    'sentry-trace'
    ]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


DEBUG = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
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

WSGI_APPLICATION = 'res_config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {}
DATABASES['default'] = dj_database_url.config()

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
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
        'accounts.authentication.PhoneNumberBackend',
        'django.contrib.auth.backends.AllowAllUsersModelBackend',
        'accounts.authentication.EmailBackend',
    ]


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv("CLOUD_NAME"),
    'API_KEY': os.getenv("API_KEY"),
    'API_SECRET': os.getenv("API_SECRET")
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