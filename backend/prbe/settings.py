from pathlib import Path
from datetime import timedelta
from corsheaders.defaults import default_headers
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
  'django-insecure-(yn*67)-5q4!73=&#3#5=n&_f!dnwul(7g-a7u3$j6h@ck7aru'
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # User Apps
    'developers.apps.DevelopersConfig',
    'brokers.apps.BrokersConfig',
    'units.apps.UnitsConfig',
    'paysched.apps.PayschedConfig',
    'affiliations.apps.AffiliationsConfig',
    'customers.apps.CustomersConfig',
    'companies.apps.CompaniesConfig',
    'documents.apps.DocumentsConfig',
    'sites.apps.SitesConfig',
    'milestones.apps.MilestonesConfig',
    'sales.apps.SalesConfig',
    'salesdetails.apps.SalesdetailsConfig',
    'dashboard.apps.DashboardConfig',

    # User
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Ensure security headers are set first
    'corsheaders.middleware.CorsMiddleware',  # Add CORS headers after security
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session handling for user sessions
    'django.middleware.common.CommonMiddleware',  # General request/response tweaks
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection for forms
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Handles authentication via session
    'django.contrib.messages.middleware.MessageMiddleware',  # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]


CORS_ALLOWED_ORIGINS = ['http://localhost:8080']
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['http://localhost:8080']
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_SECURE = True   # Disable secure cookies for dev
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True   # Disable secure cookies for dev 

 # Custom headers 
CORS_ALLOW_HEADERS = [
    'developer-id', 'company-id', 'content-type', 'authorization',
    'accept', 'accept-encoding', 'x-csrftoken', 'access-control-allow-origin',
]

# CORS_ORIGIN_ALLOW_ALL = True  # For testing purposes, allow all origins

ROOT_URLCONF = 'prbe.urls'

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
            ],
        },
    },
]



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

WSGI_APPLICATION = 'prbe.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'prdb',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Adjust as needed
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # Adjust as needed
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend
]

AUTH_USER_MODEL = 'developers.Developer'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aeronjquiambao@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'ljscdntxmmdqupmz'  # Your Gmail password or app password
