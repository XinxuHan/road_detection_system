from pathlib import Path

# Define the project root directory (two levels of directories upward)
BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# Basic Settings
# =============================================================================

# Security key, please keep it strictly confidential in the production environment!
SECRET_KEY = 'nzv30$zrxmh_j#hs@4=qr=b91i&ytz&1)%a8b6%7unyd8m@hec'

# Whether to enable the debugging mode (please turn it off in the production environment)
DEBUG = True

# The host that is allowed for access
ALLOWED_HOSTS = []

# =============================================================================
# Application definition
# =============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'home',
    'user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'YOLOv11.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Specifying the template pat
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'YOLOv11.wsgi.application'

# =============================================================================
# Database Configuration
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yolo_django',
        'USER': 'root',
        'PASSWORD': 'Yiyi20426@',  # Use your own password
    }
}

# =============================================================================
# Password validation
# =============================================================================

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

LOGIN_URL = '/login/'

# =============================================================================
# Internationalization configuration
# =============================================================================

LANGUAGE_CODE = 'en-hk'  # English (Hong Kong)

TIME_ZONE = 'Asia/Hong_Kong'  # Hong Kong Time Zone

USE_I18N = True
USE_L10N = True
USE_TZ = False

# =============================================================================
# Static file configuration
# =============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# =============================================================================
# Media File Configuration
# =============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'home' / 'media'  # The media directory in the home app
SAVEMODEL_ROOT = BASE_DIR / 'home' / 'save_models'
USER_AVATAR_ROOT = BASE_DIR / 'user' / 'media' / 'avatar'  # User avatar storage path

# =============================================================================
# CORS configuration
# =============================================================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Request source for Vue3 project
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'OPTIONS',
]

CORS_ALLOW_CREDENTIALS = True  # Vouchers allowed

# =============================================================================
# CSRF configuration
# =============================================================================

CSRF_COOKIE_SECURE = False  # The development environment allows non-HTTPS requests

# If you don't want to restrict the domain, you can let go of all cross-domain requests
CORS_ORIGIN_ALLOW_ALL = True


# =============================================================================
# LOGGING
# =============================================================================

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}
