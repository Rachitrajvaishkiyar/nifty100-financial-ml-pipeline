"""
Django settings for bluestock_project project.
Refactored for Secure Cloud Deployment.
"""

import os
from pathlib import Path
import environ
import dj_database_url

# Initialize environment variables handler
env = environ.Env()
# read .env file if it exists (primarily for local development)
environ.Env.read_env(env_file=os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY CONFIGURATION ---
# Reads SECRET_KEY from environment, drops back to a default fallback ONLY for safety
SECRET_KEY = env('SECRET_KEY', default='django-insecure-$_r60g+00(9zwkm9))bxnbybmh=axpbot19o3iv#2t+z+y11(j')

# DEBUG is True locally, but must be False in production
DEBUG = env.bool('DEBUG', default=True)

# Allows your local machine and your future deployment domains
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['127.0.0.1', 'localhost'])

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Core Application Component
    'dashboard',  
    
    # Celery Worker Ecosystem
    'django_celery_results',
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise allows Django to serve static files reliably in production without Nginx
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bluestock_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bluestock_project.wsgi.application'

# --- DATABASE CONFIGURATION ---
# In production, it parses DATABASE_URL from your cloud Postgres container.
# If unavailable (like on your MacBook Air), it defaults right back to your local Docker container.
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL', default='postgresql://bluestock_user:bluestock_password@localhost:5432/b100_warehouse')
    )
}

# --- PASSWORD VALIDATION ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC FILES ASSETS MANAGEMENT ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Optimizes static asset delivery compressing files
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- CELERY WORKER AUTOMATION CONFIGURATION ---
# Reads REDIS_URL from your production message broker seamlessly
CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIME_ZONE = 'UTC'