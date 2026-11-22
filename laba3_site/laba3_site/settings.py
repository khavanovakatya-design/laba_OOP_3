from pathlib import Path
import os
os.environ['SSL_CERT_FILE'] = r'C:\Users\1\AppData\Local\Programs\Python\Python314\Lib\site-packages\certifi\cacert.pem'

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ej*79cq!f1x&2+4ze_in6y$37%dp4sxz7qa8#oj)!w1l!#y0l_'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_filters',
    'main',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'laba3_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.cart_processor',
                'users.context_processors.wishlist_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'laba3_site.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'users.validators.CustomPasswordValidator',
        'OPTIONS': {'min_length': 8},
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Vladivostok'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/assets/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
]

MAILERS = {
    "default": {
        "BACKEND": "users.email_backend.EmailBackend",
        "OPTIONS": {
            "host": "smtp.mail.ru",
            "port": 465,
            "username": "zabrodskaiaka@mail.ru",
            "password": "Zl1w3dSgJLcnsGaXK15v",
            "use_ssl": True,
        },
    },
}

DEFAULT_FROM_EMAIL = "zabrodskaiaka@mail.ru"

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')