"""
Django settings for pyops project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "pylong$pyops@bur.ink"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
SESSION_COOKIE_NAME = "uidpylon"
# SESSION_COOKIE_DOMAIN = ".pyarn.com"
# CSRF_COOKIE_DOMAIN = ".pyarn.com"
# CSRF_TRUSTED_ORIGINS = ["https://dev.pyarn.com"]
# CSRF_TRUSTED_ORIGINS = ["https://your_CSRF_TRUSTED_ORIGINS/"]
# https://docs.djangoproject.com/en/5.1/ref/csrf/
# https://docs.djangoproject.com/en/5.1/ref/settings/#std-setting-CSRF_TRUSTED_ORIGINS
# https://docs.djangoproject.com/en/5.1/ref/settings/#session-cookie-domain


# Application definition

INSTALLED_APPS = [
    "src.pylon",
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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.joinpath("src/templates").as_posix()],
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

WSGI_APPLICATION = "main.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",  # Replace with your desired backend
        "TIMEOUT": 300,  # Cache expiration time in seconds
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ex. ROOT_URLPREFIX = pylon/
ROOT_URLPREFIX = "pylon/"
ROOT_URLCONF = "main.urls"

# for @django.contrib.auth.decorators.login_required()
LOGIN_URL = f"/{ROOT_URLPREFIX}admin/login/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = f"{ROOT_URLPREFIX}static/"
STATICFILES_DIRS = [BASE_DIR.joinpath("src/static").as_posix()]
STATIC_ROOT = BASE_DIR.joinpath("src/collectRes").as_posix()
MEDIA_ROOT = BASE_DIR.joinpath("src/media").as_posix()
MEDIA_URL = f"{ROOT_URLPREFIX}media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
