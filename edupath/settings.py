import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────────────────────────
# 1. SECURITY (Keep secret keys out of code)
# ──────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ──────────────────────────────────────────────────────────────────
# 2. INSTALLED APPS (No changes needed)
# ──────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'accounts',
    'schools',
    'students',
    'advertising',
]

# ──────────────────────────────────────────────────────────────────
# 3. MIDDLEWARE (WhiteNoise for static files, security first)
# ──────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',          # For static files
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',           # Protects against CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Prevents clickjacking
]

ROOT_URLCONF = 'edupath.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'edupath.context_processors.admin_stats',
            ],
        },
    },
]

WSGI_APPLICATION = 'edupath.wsgi.application'

# ──────────────────────────────────────────────────────────────────
# 4. DATABASE (PostgreSQL on Render, SQLite locally)
# ──────────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    # Production: Render PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)
    }
else:
    # Development: SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ──────────────────────────────────────────────────────────────────
# 5. PASSWORD VALIDATION (Strong passwords)
# ──────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ──────────────────────────────────────────────────────────────────
# 6. INTERNATIONALIZATION
# ──────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Kampala'
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────────────────────────
# 7. STATIC & MEDIA FILES
# ──────────────────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ──────────────────────────────────────────────────────────────────
# 8. CUSTOM USER MODEL
# ──────────────────────────────────────────────────────────────────
AUTH_USER_MODEL = 'accounts.SchoolUser'

# ──────────────────────────────────────────────────────────────────
# 9. REST FRAMEWORK (Simplified for now)
# ──────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# ──────────────────────────────────────────────────────────────────
# 10. CORS (Allow only your frontend domain in production)
# ──────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8000,http://127.0.0.1:8000').split(',')

# ──────────────────────────────────────────────────────────────────
# 11. SECURITY HEADERS (For production, when DEBUG=False)
# ──────────────────────────────────────────────────────────────────
if not DEBUG:
    SECURE_SSL_REDIRECT = True                      # Force HTTPS
    SESSION_COOKIE_SECURE = True                    # Secure session cookie
    CSRF_COOKIE_SECURE = True                       # Secure CSRF cookie
    SECURE_BROWSER_XSS_FILTER = True                # XSS protection
    SECURE_CONTENT_TYPE_NOSNIFF = True              # Prevent MIME sniffing
    X_FRAME_OPTIONS = 'DENY'                        # Prevent clickjacking
    SECURE_HSTS_SECONDS = 31536000                  # 1 year HSTS
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ──────────────────────────────────────────────────────────────────
# 12. DEFAULT PRIMARY KEY FIELD
# ──────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'