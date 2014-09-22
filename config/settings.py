"""
Django settings for config project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ty4yiuv*lkz)0o9#6*%cnswoppl5#_(lf-d(kzn-$&_ya(7&gx'
SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

ANONYMOUS_USER_ID = 1

# Application definition

INSTALLED_APPS = (
    'djangular',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    # 'debug_toolbar',
    'mptt',
    'app',
    'liang.modules.api',
    'liang.modules.accounts',
    'liang.modules.comments',
    'liang.modules.peoples',
    'liang.modules.tagging',
    'liang.modules.articles',
    'liang.modules.likes',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'
APPEND_SLASH = False

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
# 'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'jinshishu',
#         'USER': 'root',
#         'PASSWORD': '',
#         'OPTIONS': {
#             'autocommit': True,
#         },
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Auth
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/auth/login'
LOGOUT_URL = '/auth/logout'
LOGIN_REDIRECT_URL = '/'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    # 'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    # 'django.contrib.auth.hashers.BCryptPasswordHasher',
    # 'django.contrib.auth.hashers.SHA1PasswordHasher',
    # 'django.contrib.auth.hashers.MD5PasswordHasher',
    # 'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    # 'django.contrib.auth.hashers.CryptPasswordHasher'
)

# Email
# EMAIL_HOST = 'smtp.brohere.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = 'notify@brohere.com'
# EMAIL_HOST_PASSWORD = 'brohere2014'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'leon.shao@brohere.com'
EMAIL_HOST_PASSWORD = 'loveyu1314'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)


# Upload
MEDIA_URL = "/static/storage/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/storage")
FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)
# DEFAULT_FILE_STORAGE = "app.storage.CloudStorage"

QINIU_ACCESS_KEY = "cSlEbes-zd-cr0xbIgzXrnKA7l5FoQL3IPWxPgM6"
QINIU_SECRET_KEY = "3rjQYp-5Qbc8nL-cP9o3qfRUCrWH9WX18em4iih0"
QINIU_BUCKET_NAME = "brohere"

# Template
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'liang.modules.api.context_processors.contents',
)


# Comment
COMMENTS_APP = 'liang.modules.comments'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
