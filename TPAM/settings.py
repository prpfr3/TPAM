"""
Django settings for TPAM solution.
More info on settings:-
https://docs.djangoproject.com/en/4.2/topics/settings/
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import configparser
import dj_database_url

# My Settings
LOGIN_URL = '/users/login'
# __file__ is the full path of the current file, settings.py
# os.path.dirname is the directory of the current file and dirname x 2 the directory one level up
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
# Required as from Django 4.2
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_extensions',
    'smart_selects',

    # Third Party Apps
    'crispy_forms',
    'crispy_bootstrap5',
    'django_bootstrap5',
    'rest_framework',
    'rest_framework.authtoken',
    'sorl.thumbnail',
    'tinymce',

    # Myapps
    'aircraft',
    'api',
    'companies',
    'locations',
    'locos',
    'mainmenu',
    'notes',
    'mvs',
    'people',
    'rtt',
    'storages',
    'storymaps',
    'TPAM',
    'users',
    'vehicles'
]

# Initiate token authentication for REST APIs
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # To enforce token based authentication
        'rest_framework.authentication.TokenAuthentication',
        # Needed if browser sessions also used in parallel to token based authentication
        'rest_framework.authentication.SessionAuthentication',
    ]
}

# Middleware framework
# https://docs.djangoproject.com/en/4.2/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'TPAM.urls'
CART_SESSION_ID = 'cart'

# Template configuration
# https://docs.djangoproject.com/en/4.2/topics/templates/
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

WSGI_APPLICATION = 'TPAM.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Following theoretically not needed for production and/or AWS S3. Best to retain though.
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    # Note the theme 'modern' is deprecated - do not use
    # https://www.tiny.cloud/docs/migration-from-4x/#themes
    'theme': 'silver',
    'plugins': '''
      textcolor save link image media preview codesample contextmenu table code lists fullscreen insertdatetime nonbreaking contextmenu directionality searchreplace wordcount visualblocks visualchars code fullscreen autolink lists charmap print hr anchor pagebreak
     ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code | h1 h2 h3 |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Establish the current working directory to determine whether settings should be for a production or local server.
cwd = os.getcwd()
if cwd == '/app' or cwd.startswith('/tmp'):  # PRODUCTION SETTINGS
    print('Using production settings from settings.py')

    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
    DEBUG = False  # Always runs as False in Production
    ALLOWED_HOSTS = ['tpam-production.up.railway.app']

    DATABASES = {
        'default': dj_database_url.config(default='postgres://localhost')
    }

    DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

    # Honor the 'X-Forwarded-Proto' header for request.is_secure().
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Get Other API Keys
    app_id = os.environ['OTAPI_APP_ID']
    api_key = os.environ['OTAPI_API_KEY']

    # AWS S3 settings
    AWS_STORAGE_BUCKET_NAME = 'django-tpam-paulf'
    AWS_S3_REGION_NAME = 'eu-west-2'  # e.g. us-east-2
    AWS_DEFAULT_ACL = None
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

    # Tell django-storages the domain to use to refer to static files.
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # specify the Django storage classes

    STATICFILES_LOCATION = 'staticfiles'  # The directory name in S3
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'  # For AWS
#   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # For Whitenoise Static Files Storage
    MEDIAFILES_LOCATION = 'media'
    # ideally this would be called mediafiles_storage in django but it isn't !
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': ('%(asctime)s [%(process)d] [%(levelname)s] '
                           'pathname=%(pathname)s lineno=%(lineno)s '
                           'funcname=%(funcName)s %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }

else:  # DEVELOPMENT SETTINGS
    msg = (
        f'Using development/local settings from settings.py.\n'
        f'Base directory is {BASE_DIR}.'
        f'Static directory is {STATIC_ROOT}.\n'
    )
    print(msg)

    config = configparser.ConfigParser()
    KEYS_DIR = os.path.join("D:\\Data", "API_Keys")
    config.read(os.path.join(KEYS_DIR, "TPAMWeb.ini"))
    SECRET_KEY = config['Django']['tpam_secret_key']
    INSTALLED_APPS += ['django.contrib.gis',]

    DEBUG = True

    if DEBUG:
        MIDDLEWARE = [
            'debug_toolbar.middleware.DebugToolbarMiddleware',] + MIDDLEWARE
        INSTALLED_APPS += ['debug_toolbar',]
        INTERNAL_IPS = ["127.0.0.1"]
        DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False, }
        # Following addresses potential problem with debug toolbar display
        import mimetypes
        mimetypes.add_type("application/javascript", ".js", True)

    ALLOWED_HOSTS = []
    # GDAL_LIBRARY_PATH = r'C:\\OSGeo4W64\\bin\\gdal301'

    db_pswd = config['MySQL']['p']

    # Get Other API keys
    OTAPI_APP_ID = config['opentransport']['app_id']
    OTAPI_API_KEY = config['opentransport']['api_key']

    DATABASE_URL = f'postgresql://postgres:{db_pswd}@localhost/TPAM'

    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'TPAM',
            'USER': 'postgres',
            'PASSWORD': db_pswd,
            'HOST': 'localhost',
            'PORT': '5432', }
    }
