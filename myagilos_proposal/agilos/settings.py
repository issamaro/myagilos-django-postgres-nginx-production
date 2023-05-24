"""
Django settings for agilos project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "changeme")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", 0)))

# ADMINS = []
# if ADMINS_ENV := os.environ.get("ADMINS", None):
#     ADMINS_ENV = [
#         (f"{admin.split(':')[0].split('_')[0].capitalize()} {admin.split(':')[0].split('_')[1].capitalize()}", admin.split(":")[1])
#         for admin in ADMINS_ENV.split("%")
#     ]

ALLOWED_HOSTS = []
if ALLOWED_HOSTS_ENV := os.environ.get("ALLOWED_HOSTS", None):
    ALLOWED_HOSTS = [host.strip().lower() for host in ALLOWED_HOSTS_ENV.split(",")]

# HTTPS SETTINGS
if bool(int(os.environ.get("HTTPS_ON", False))):
    SESSION_COOKIE_SECURE = bool(int(os.environ.get("SESSION_COOKIE_SECURE", 0)))
    CSRF_COOKIE_SECURE = bool(int(os.environ.get("CSRF_COOKIE_SECURE", 0)))
    SECURE_SSL_REDIRECT = bool(int(os.environ.get("SECURE_SSL_REDIRECT", 0)))
else:
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
# HSTS SETTINGS
if bool(int(os.environ.get("HSTS_ON", False))):
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 0))
    SECURE_HSTS_PRELOAD = bool(int(os.environ.get("SECURE_HSTS_PRELOAD", 0)))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = bool(int(os.environ.get("SECURE_HSTS_INCLUDE_SUBDOMAINS", 0)))
else:
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_PRELOAD = False
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    
SESSION_COOKIE_AGE = os.environ.get("SESSION_COOKIE_AGE", "1209600")
# Application definition

INSTALLED_APPS = [
    "django_feather",
    "consultants",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "agilos.urls"

# Redirection
LOGIN_URL = "consultants:login"
LOGIN_REDIRECT_URL = "consultants:home"
LOGOUT_REDIRECT_URL = "consultants:home"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "agilos.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "db",
        "NAME": "n",
        "USER": "u",
        "PASSWORD": "p"
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/static/"
MEDIA_URL = "/static/media/"

STATIC_ROOT = "/vol/web/static"
MEDIA_ROOT = "/vol/web/media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"