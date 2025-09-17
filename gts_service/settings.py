"""
Django settings for gts_service project.
"""

import os
import environ

# Initialize environment variables
env = environ.Env(
    # set default values in case .env is missing
    DEBUG=(bool, False),
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "w#u9z&7q0o8f^k2v!3l%p@4x6t$g+1d5r^h!"

# DEBUG setting
DEBUG = env.bool("DEBUG")  # defaults to False if not set in .env

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "gts_service",
    "bootstrap3",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gts_service.urls"

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

WSGI_APPLICATION = "gts_service.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"

# OpenSCAD executable (Windows)
OPENSCAD_EXECUTABLE = env.str("SCAD_EXECUTABLE", default=r".\openscad\openscad.exe")

# Show error if not found
if not os.path.isfile(OPENSCAD_EXECUTABLE):
    print(f"Warning: OpenSCAD executable not found at {OPENSCAD_EXECUTABLE}")
    input("Press enter to exit...")
