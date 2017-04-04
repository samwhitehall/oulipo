"""
Django settings for oulipo project.
"""

import os

from oulipo.secrets import SECRET_KEY

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = False

ALLOWED_HOSTS = ['oulipo.samwhitehall.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',

    'poem',
]

MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'oulipo.urls'

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

WSGI_APPLICATION = 'wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-uk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

# Celery settings
BROKER_URL = 'amqp://guest:guest@rabbitmq'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TASK_RESULT_EXPIRES = 30

CELERY_RESULT_BACKEND = 'rpc://'
CELERY_RESULT_PERSISTENT = False

CELERY_TIMEOUT = 5

# CORS origin settings
CORS_ORIGIN_WHITELIST = ['oulipo.samwhitehall.com']


# Overwrite some variables for development
if os.environ.get('DEVELOPMENT'):
    print "---DEVELOPMENT MODE---"
    DEBUG = True
    ALLOWED_HOSTS = ['*']
    CORS_ORIGIN_ALLOW_ALL = True
