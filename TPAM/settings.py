"""
Django settings for TPAM solution.

More info on settings:-
https://docs.djangoproject.com/en/3.1/topics/settings/
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import configparser
import dj_database_url

# My Settings
LOGIN_URL = '/users/login'
#Note that the use of dirname twice has the effect of making the Base Directory one level up from that in which settings.py resides
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #__file__ is the current path of imports
print('BASE_DIR = ', BASE_DIR)
DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
DEFAULT_AUTO_FIELD='django.db.models.AutoField' #Required as from Django 3.2

# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_extensions',
    'smart_selects',

    #Third Party Apps
    'bootstrap3',
    'crispy_forms',
    'crispy_bootstrap5',
    'debug_toolbar',
    'django_bootstrap5',
    'rest_framework',
    'rest_framework.authtoken',
    'sorl.thumbnail',
    'tinymce',

    #Myapps
    'aircraft',
    'api',
    'locos',
    'mainmenu',
    'maps',
    'mvs',
    'rtt',
    'storages',
    'TPAM',
    'users',
    'vehicles'
]

#The following ensures that token authentication is used for REST APIs
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication', #To enforce token based authentication
        'rest_framework.authentication.SessionAuthentication', #Needed if browser sessions also used in parallel to token based authentication
        ]
}

# Middleware framework
# https://docs.djangoproject.com/en/2.1/topics/http/middleware/
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',    
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
#CRISPY_TEMPLATE_PACK = 'bootstrap4'
#GEOIP_PATH = os.path.join(BASE_DIR, 'geoip')

# Template configuration
# https://docs.djangoproject.com/en/2.1/topics/templates/
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

# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images) and Media files (images maintainable by users of the applicaction)
## https://docs.djangoproject.com/en/3.1/howto/static-files/

#Theoretically not used on an AWS S3 storage solution but in practice best to retain. Often expected by runserver (though normally only used on a local implementation)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

#Setting for django-bootstrap3 to include a required Javascript library

#BOOTSTRAP3 = {
#  'include_jquery': True,}

TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    #Note the theme CANNOT be modern which is deprecated
    #https://www.tiny.cloud/docs/migration-from-4x/#themes
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
print(f'{cwd=}')
if cwd == '/app' or cwd[:4] == '/tmp':
  print('Using production settings from settings.py')

  SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
  DEBUG = False #Always runs as False in Production
  ALLOWED_HOSTS = ['tpam.herokuapp.com']
 
  DATABASES = {
      #'default': dj_database_url.config(default='postgres://localhost')
      'default': dj_database_url.config(default='postgis://localhost')
  }
    
  # Honor the 'X-Forwarded-Proto' header for request.is_secure().
  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

  # Get Other API Keys
  app_id = os.environ['OTAPI_APP_ID']
  api_key = os.environ['OTAPI_API_KEY']

  #AWS S3 settings
  AWS_STORAGE_BUCKET_NAME = 'django-tpam-paulf'
  AWS_S3_REGION_NAME = 'eu-west-2'  # e.g. us-east-2
  AWS_DEFAULT_ACL = None
  AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
  AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

  # Tell django-storages the domain to use to refer to static files.
  AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

  #specify the Django storage classes

  STATICFILES_LOCATION = 'static'
#   STATICFILES_STORAGE = 'custom_storages.StaticStorage' #For AWS
  STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # For Whitenoise Static Files Storage
  MEDIAFILES_LOCATION = 'media'
  DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage' #ideally this would be called mediafiles_storage in django but it isn't !

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

else:
  print('Using development/local settings from settings.py.\nStatic directory is {} given a base directory of {}'.format(STATIC_ROOT, BASE_DIR))

  config = configparser.ConfigParser()
  KEYS_DIR = os.path.join("D:\\Data", "API_Keys")
  config.read(os.path.join(KEYS_DIR, "TPAMWeb.ini"))
  SECRET_KEY = config['Django']['tpam_secret_key']  
  DEBUG = True
  ALLOWED_HOSTS = []
  INTERNAL_IPS = ["127.0.0.1"] #Required for Django Debug
#   GDAL_LIBRARY_PATH = r'C:\\OSGeo4W64\\bin\\gdal301' 

  db_pswd = config['MySQL']['p']

  # E-mail
  # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#   EMAIL_HOST = 'smtp.gmail.com'
#   EMAIL_HOST_USER = config['Email']['address']
#   EMAIL_HOST_PASSWORD = config['Email']['password']
#   EMAIL_PORT = 587
#   EMAIL_USE_TLS = True
 
  #Get Other API keys
  OTAPI_APP_ID = config['opentransport']['app_id']
  OTAPI_API_KEY = config['opentransport']['api_key']

  DATABASE_URL = 'postgresql://postgres:' + db_pswd + '@localhost/TPAM'

  DATABASES = {
      #'default': {
          #'ENGINE': 'django.db.backends.sqlite3',
          #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

      'default': {
        #   'ENGINE': 'django.db.backends.postgresql',
          'ENGINE': 'django.contrib.gis.db.backends.postgis',
          'NAME': 'TPAM',
          'USER': 'postgres',
          'PASSWORD': db_pswd,
          'HOST': 'localhost',
          'PORT': '5432',}

      #'default': {
      #    'ENGINE': 'django.db.backends.mysql',
      #    'NAME': 'railways',
      #    'USER': 'dbadmin',
      #    'PASSWORD': db_pswd,
      #    'HOST': 'localhost',
      #    'PORT': '3306',}
  }