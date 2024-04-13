"""
More info on settings:-
https://docs.djangoproject.com/en/5.0/topics/settings/
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import configparser

# import dj_database_url

# My Settings
LOGIN_URL = "/users/login"
# __file__ is the full path of the current file, settings.py
# os.path.dirname is the directory of the current file and dirname x 2 the directory one level up
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
# Required as from Django 4.2
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-INSTALLED_APPS
INSTALLED_APPS = [
    "djangocms_admin_style",  # django-cms requirement. Must be before django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django_extensions",
    "smart_selects",
    # django-cms requirements
    "django.contrib.sites",
    "cms",  # A core CMS module
    "menus",  # A core CMS module
    "treebeard",  # Used for CMS page tree structures
    "sekizai",
    "filer",
    "easy_thumbnails",
    "djangocms_frontend",
    "djangocms_frontend.contrib.accordion",
    "djangocms_frontend.contrib.alert",
    "djangocms_frontend.contrib.badge",
    "djangocms_frontend.contrib.card",
    "djangocms_frontend.contrib.carousel",
    "djangocms_frontend.contrib.collapse",
    "djangocms_frontend.contrib.content",
    "djangocms_frontend.contrib.grid",
    "djangocms_frontend.contrib.image",
    "djangocms_frontend.contrib.jumbotron",
    "djangocms_frontend.contrib.link",
    "djangocms_frontend.contrib.listgroup",
    "djangocms_frontend.contrib.media",
    "djangocms_frontend.contrib.tabs",
    "djangocms_frontend.contrib.utilities",
    "djangocms_text_ckeditor",
    "djangocms_file",
    "djangocms_picture",
    "djangocms_video",
    "djangocms_googlemap",
    "djangocms_snippet",
    "djangocms_style",
    "djangocms_alias",
    "djangocms_versioning",  # Third Party Apps
    "crispy_forms",
    "crispy_bootstrap5",
    "django_bootstrap5",
    "rest_framework",
    "rest_framework.authtoken",
    "sorl.thumbnail",
    "tinymce",
    # Myapps
    "api",
    "companies",
    "locations",
    "locos",
    "mainmenu",
    "notes",
    "mvs",
    "people",
    "rtt",
    "storages",
    "storymaps",
    "timelines",
    "TPAM",
    # "ukheritage", "Commented out to remove GDAL dependencies"
    "users",
    # "vehicles", "Commented out because smart selects does not work with Django 5"
]

# django cms requirements
SITE_ID = 1  # Needed for django-cms use of django.contrib.sites
CMS_CONFIRM_VERSION4 = True  # Makes sure you don't run migrate on a V3 cms project
X_FRAME_OPTIONS = "SAMEORIGIN"
CMS_TEMPLATES = [
    ("base.html", "Home page template"),
]
THUMBNAIL_HIGH_RESOLUTION = True
USE_I18N = False

# Enable permissions
# https://docs.django-cms.org/en/release-4.1.x/topics/permissions.html
# https://docs.django-cms.org/en/latest/explanation/permissions.html
CMS_PERMISSION = True

THUMBNAIL_PROCESSORS = (
    "easy_thumbnails.processors.colorspace",
    "easy_thumbnails.processors.autocrop",
    "filer.thumbnail_processors.scale_and_crop_with_subject_location",
    "easy_thumbnails.processors.filters",
)

# Initiate token authentication for REST APIs
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # To enforce token based authentication
        "rest_framework.authentication.TokenAuthentication",
        # Needed if browser sessions also used in parallel to token based authentication
        "rest_framework.authentication.SessionAuthentication",
    ]
}

# Middleware framework
# https://docs.djangoproject.com/en/4.2/topics/http/middleware/
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "cms.middleware.utils.ApphookReloadMiddleware",  # Optional for django-cms
    "django.middleware.locale.LocaleMiddleware",  # Required for django-cms
    "cms.middleware.user.CurrentUserMiddleware",  # Required for django-cms
    "cms.middleware.page.CurrentPageMiddleware",  # Required for django-cms
    "cms.middleware.toolbar.ToolbarMiddleware",  # Required for django-cms
    "cms.middleware.language.LanguageCookieMiddleware",  # Required for django-cms
]

ROOT_URLCONF = "TPAM.urls"
CART_SESSION_ID = "cart"

# Template configuration
# https://docs.djangoproject.com/en/4.2/topics/templates/
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # "DIRS": [],
        "DIRS": [
            os.path.join(BASE_DIR, "TPAM", "templates"),
        ],  # Amendment for django-cms
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",  # Added for django-cms
                "sekizai.context_processors.sekizai",  # Added for django-cms
                "cms.context_processors.cms_settings",  # Added for django-cms as cms check says necessary
            ],
        },
    },
]

WSGI_APPLICATION = "TPAM.wsgi.application"

# Password validation
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
LANGUAGES = [
    ("en", "English"),
    # ("de", "German"),
    # ("it", "Italian"),
]
LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Following theoretically not needed for production and/or AWS S3. Best to retain though.
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

TINYMCE_DEFAULT_CONFIG = {
    "content_css": [
        "https://use.fontawesome.com/releases/v5.15.4/css/all.css",
        "https://use.fontawesome.com/releases/v5.15.4/css/v4-shims.css",
        "https://fonts.googleapis.com/css?family=Montserrat",
        "https://fonts.googleapis.com/css?family=Raleway",
    ],
    "font_formats": "Montserrat=montserrat,arial,sans-serif;Raleway=raleway,arial,sans-serif",
    "height": 360,
    "width": 1120,
    "cleanup_on_startup": True,
    "custom_undo_redo_levels": 20,
    "selector": "textarea",
    # Note the theme 'modern' is deprecated - do not use
    # https://www.tiny.cloud/docs/migration-from-4x/#themes
    "theme": "silver",
    "plugins": """
      textcolor save link image media preview codesample contextmenu table code lists fullscreen insertdatetime nonbreaking contextmenu directionality searchreplace wordcount visualblocks visualchars code autolink lists charmap print hr anchor pagebreak
     """,
    "toolbar1": """
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample
            """,
    "toolbar2": """
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code | h1 h2 h3 |
            """,
    "contextmenu": "formats | link image",
    "menubar": True,
    "statusbar": True,
}


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Establish the current working directory to determine whether settings should be for a production or local server.
cwd = os.getcwd()
if cwd == "/app" or cwd.startswith("/home"):  # PRODUCTION SETTINGS
    print("Using production settings from settings.py")

    # Get all the config variables
    config = configparser.ConfigParser()
    passwords_file = "/root/.env"
    try:
        config.read(passwords_file)
        SECRET_KEY = config["Django"]["tpam_secret_key"]
        DATABASE_KEY = config["Django"]["database_key"]
        AWS_ACCESS_KEY_ID = config["Django"]["aws_access_key_id"]
        AWS_SECRET_ACCESS_KEY = config["Django"]["aws_secret_access_key"]
        OTAPI_APP_ID = config["opentransport"]["app_id"]
        OTAPI_API_KEY = config["opentransport"]["api_key"]
    except FileNotFoundError:
        # Handle file not found error
        print("Error: .env file not found")
    except configparser.NoSectionError:
        # Handle missing section error
        print("Error: [Django] section not found in .env file")
    except configparser.NoOptionError:
        # Handle missing option error
        print("Error: One of the keys not found in [Django] section of .env file")

    DEBUG = False  # Always runs as False in Production

    # Find out what the IP addresses are at run time
    # This is necessary because otherwise Gunicorn will reject the connections
    import netifaces

    def ip_addresses():
        ip_list = []
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            for x in (netifaces.AF_INET, netifaces.AF_INET6):
                if x in addrs:
                    ip_list.append(addrs[x][0]["addr"])
        return ip_list

    print(ip_addresses())
    ALLOWED_HOSTS = ip_addresses()

    # DATABASES = {"default": dj_database_url.config(default="postgres://localhost")}

    # DATABASES["default"]["ENGINE"] = "django.db.backends.postgresql"

    # DATABASE_KEY = config["Django"]["database_key"]

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "django",
            "USER": "django",
            "PASSWORD": DATABASE_KEY,
            "HOST": "localhost",
            "PORT": "5432",
            "OPTIONS": {"sslmode": "require"},
        }
    }

    # Honor the 'X-Forwarded-Proto' header for request.is_secure().
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # AWS S3 settings
    AWS_STORAGE_BUCKET_NAME = "django-tpam-paulf"
    AWS_S3_REGION_NAME = "eu-west-2"  # e.g. us-east-2
    AWS_DEFAULT_ACL = None

    # Tell django-storages the domain to use to refer to static files.
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

    # specify the Django storage classes

    STATICFILES_LOCATION = "staticfiles"  # The directory name in S3
    STATICFILES_STORAGE = "custom_storages.StaticStorage"  # For AWS
    #   STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # For Whitenoise Static Files Storage
    MEDIAFILES_LOCATION = "media"
    # ideally this would be called mediafiles_storage in django but it isn't !
    DEFAULT_FILE_STORAGE = "custom_storages.MediaStorage"

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": (
                    "%(asctime)s [%(process)d] [%(levelname)s] "
                    "pathname=%(pathname)s lineno=%(lineno)s "
                    "funcname=%(funcName)s %(message)s"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {"format": "%(levelname)s %(message)s"},
        },
        "handlers": {
            "null": {
                "level": "DEBUG",
                "class": "logging.NullHandler",
            },
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django.request": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

else:  # DEVELOPMENT SETTINGS
    msg = (
        f"Using development/local settings from settings.py.\n"
        f"Base directory is {BASE_DIR}."
        f"Static directory is {STATIC_ROOT}.\n"
    )
    print(msg)

    config = configparser.ConfigParser()
    KEYS_DIR = os.path.join("D:\\Data", "API_Keys")
    config.read(os.path.join(KEYS_DIR, "TPAMWeb.ini"))
    SECRET_KEY = config["Django"]["tpam_secret_key"]

    DEBUG = True

    if DEBUG:
        MIDDLEWARE = [
            "debug_toolbar.middleware.DebugToolbarMiddleware",
        ] + MIDDLEWARE
        INSTALLED_APPS += [
            "debug_toolbar",
        ]
        INTERNAL_IPS = ["127.0.0.1"]
        DEBUG_TOOLBAR_CONFIG = {
            "INTERCEPT_REDIRECTS": False,
        }
        # Following addresses potential problem with debug toolbar display
        import mimetypes

        mimetypes.add_type("application/javascript", ".js", True)

    ALLOWED_HOSTS = []
    # GDAL_LIBRARY_PATH = r'C:\\OSGeo4W64\\bin\\gdal301'

    db_pswd = config["MySQL"]["p"]

    # Get Other API keys
    OTAPI_APP_ID = config["opentransport"]["app_id"]
    OTAPI_API_KEY = config["opentransport"]["api_key"]

    # DATABASE_URL = f"postgresql://postgres:{db_pswd}@localhost/TPAM"

    # INSTALLED_APPS += [
    #     "django.contrib.gis",
    # ]  # If GDAL: installed

    DATABASES = {
        "default": {
            # "ENGINE": "django.contrib.gis.db.backends.postgis",  # If GDAL installed
            "ENGINE": "django.db.backends.postgresql",  # If GDAL not installed
            "NAME": "TPAM",
            "USER": "postgres",
            "PASSWORD": db_pswd,
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.mysql",
    #         "NAME": "tpam",
    #         "USER": "root",
    #         "PASSWORD": "",
    #         "HOST": "localhost",
    #         "PORT": "",
    #     }
    # }
