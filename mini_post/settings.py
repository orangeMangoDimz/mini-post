"""
Django settings for mini_post project.

Generated by 'django-admin startproject' using Django 2.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@zgq^jhf^btpy11l+o2doom7o0@9a#(zgosem8=*1tn!9o91g*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Take environment variables from .env file
environ.Env.read_env()
env = environ.Env()


# Application definition

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'config',
    'likes',
    'posts',
    'comments',
    'activities',
    "api",
    "rest_framework",
    "bootstrap5",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'config.middleware.AuthRequiredMiddleware',
]

ROOT_URLCONF = 'mini_post.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

ASGI_APPLICATION = "mini_post.asgi.application"
WSGI_APPLICATION = 'mini_post.wsgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

LOGGING_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGGING_DIR, exist_ok=True)
LOGGING = {
    'version': 1, 
    'disable_existing_loggers': False, 
    'formatters': {
        'verbose': {
            'format': '[{asctime}] [{levelname}] {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': env('DJANGO_LOG_LEVEL'),
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'system': {
            'level': env('DJANGO_LOG_LEVEL'),
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'system.log'),
            'formatter': 'verbose',
        },
        'auth': {
            'level': env('DJANGO_LOG_LEVEL'),
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'auth_user.log'),
            'formatter': 'verbose',
        },
        'post': {
            'level': env('DJANGO_LOG_LEVEL'),
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'post.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'system'],
            'level':env('DJANGO_LOG_LEVEL'),
            'propagate': False,
        },
        'mini_post.views': {  
            'handlers': ['console', 'auth'],
            'level': env('DJANGO_LOG_LEVEL'), 
            'propagate': False,
        },
        'api': {  
            'handlers': ['console', 'post'],
            'level': env('DJANGO_LOG_LEVEL'), 
            'propagate': False,
        },
    },
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'), 
        'USER':env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'), 
        'PORT': env('DB_PORT'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = "/media/"
MEDIA_ROOT = "media"

