import os
from pathlib import Path
from dotenv import load_dotenv
from icecream import ic

# Build paths inside the project like this: ROOT_DIR / 'subdir'.
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent
APPS_DIR = ROOT_DIR / "b2d_ventures"

# Load environment variables from .env file
load_dotenv(ROOT_DIR / '.env')

# GENERAL
# -----------------------------------------------------------------------------
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default_secret_key')

TIME_ZONE = "Asia/Bangkok"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

# Application definition

INSTALLED_APPS = [
  "b2d_ventures.apps.B2DVenturesConfig",
  "b2d_ventures.app",
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",
  "rest_framework",
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

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
  'default': {
      'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
      'NAME': os.getenv('DB_NAME', ROOT_DIR / 'db.sqlite3'),
      'USER': os.getenv('DB_USER', ''),
      'PASSWORD': os.getenv('DB_PASSWORD', ''),
      'HOST': os.getenv('DB_HOST', ''),
      'PORT': os.getenv('DB_PORT', ''),
  }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'app.User'
AUTHENTICATION_BACKENDS = [
  "django.contrib.auth.backends.ModelBackend",
]
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

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework Configuration
# django-rest-framework
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
  "EXCEPTION_HANDLER": "rest_framework_json_api.exceptions.exception_handler",
  "DEFAULT_PARSER_CLASSES": ("rest_framework_json_api.parsers.JSONParser",),
  "DEFAULT_RENDERER_CLASSES": (
      "rest_framework_json_api.renderers.JSONRenderer",
      "rest_framework.renderers.BrowsableAPIRenderer",
  ),
  "DEFAULT_METADATA_CLASS": "rest_framework_json_api.metadata.JSONAPIMetadata",
  "DEFAULT_FILTER_BACKENDS": (
      "rest_framework_json_api.filters.QueryParameterValidationFilter",
      "rest_framework_json_api.filters.OrderingFilter",
      "rest_framework_json_api.django_filters.DjangoFilterBackend",
      "rest_framework.filters.SearchFilter",
  ),
  "SEARCH_PARAM": "filter[search]",
  "TEST_REQUEST_RENDERER_CLASSES": (
      "rest_framework_json_api.renderers.JSONRenderer",
  ),
  "TEST_REQUEST_DEFAULT_FORMAT": "vnd.api+json",
}

# Google OAuth Configuration
TOKEN_URL = os.getenv("TOKEN_URL", "")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("REDIRECT_URI", "")

# ALLOWED_HOSTS configuration
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')