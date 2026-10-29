"""
More info on settings:-
https://docs.djangoproject.com/en/5.0/topics/settings/
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import configparser

# My Settings
LOGIN_URL = "/users/login"
# __file__ is the full path of the current file, settings.py
# os.path.dirname is the directory of the current file and dirname x 2 the directory one level up
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # points to TPAM

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

DATAIO_DIR = os.path.join("D:\\Data", "TPAM")
# Required as from Django 4.2
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-INSTALLED_APPS
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

config = configparser.ConfigParser()

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django_extensions",
    "smart_selects",
    # Third Party Apps
    "crispy_forms",
    "crispy_bootstrap5",
    "django_bootstrap5",
    "rest_framework",
    "rest_framework.authtoken",
    "tinymce",
    # Myapps
    "api",
    "brmsra",
    "companies",
    "locations",
    "locos",
    "mainmenu",
    "notes",
    "people",
    "rtt",
    "storymaps",
    "TPAM",
    "users",
]

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
    "TPAM.middleware.LoginRequiredMiddleware",  # Custom middleware - forces login
]

ROOT_URLCONF = "TPAM.urls"

# Template configuration
# https://docs.djangoproject.com/en/4.2/topics/templates/
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
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
]
LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

GDAL_INSTALLED = True

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
    "cleanup_on_startup": False,  # Don't strip iframe HTML at load
    "cleanup": False,  # Disable auto-cleanup
    "verify_html": False,  # Allow non-standard HTML (important for iframes)
    "custom_undo_redo_levels": 20,
    "selector": "textarea.tinymce-editor",
    "theme": "silver",
    "plugins": """
        textcolor save link image media preview codesample contextmenu table code lists fullscreen
        insertdatetime nonbreaking directionality searchreplace wordcount visualblocks visualchars
        autolink lists charmap print hr anchor pagebreak
    """,
    "toolbar1": """
        fullscreen preview bold italic underline | fontselect fontsizeselect |
        forecolor backcolor | alignleft alignright aligncenter alignjustify |
        indent outdent | bullist numlist table | link image media | codesample
    """,
    "toolbar2": """
        visualblocks visualchars | charmap hr pagebreak nonbreaking anchor |
        code | h1 h2 h3
    """,
    "contextmenu": "formats | link image",
    "menubar": True,
    "statusbar": True,
    "editor_deselector": "mceNoEditor",
    "valid_elements": "*[*]",  # Keep this broad rule
    # Explicitly allow iframes
    "extended_valid_elements": "iframe[src|width|height|frameborder|allowfullscreen|allow|style|scrolling]",
    "valid_children": "+body[iframe]",  # Allow iframe directly inside body
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
        OTAPI_APP_ID = config["opentransport"]["app_id"]
        OTAPI_API_KEY = config["opentransport"]["api_key"]
    except FileNotFoundError:
        print("Error: .env file not found")
    except configparser.NoSectionError:
        print("Error: [Django] section not found in .env file")
    except configparser.NoOptionError:
        print("Error: One of the keys not found in [Django] section of .env file")

    GDAL_LIBRARY_PATH = os.getenv("GDAL_LIBRARY_PATH", "/lib/libgdal.so")
    GEOS_LIBRARY_PATH = os.getenv(
        "GEOS_LIBRARY_PATH", "/lib/x86_64-linux-gnu/libgeos_c.so"
    )

    DEBUG = False  # Always runs as False in Production

    ALLOWED_HOSTS = [
        "up-and-down-the-line.uk",
        "www.up-and-down-the-line.uk",
        "134.122.98.236",
        "localhost",
    ]

    INSTALLED_APPS += [
        "django.contrib.gis",
    ]

    # "ENGINE": "django.db.backends.postgresql_psycopg2",
    DATABASES = {
        "default": {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "NAME": "tpam",
            "USER": "django",
            "PASSWORD": DATABASE_KEY,
            "HOST": "localhost",
            "PORT": "5432",
            "OPTIONS": {"sslmode": "require"},
        }
    }

    # Honor the 'X-Forwarded-Proto' header for request.is_secure().
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

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
    )
    print(msg)

    config = configparser.ConfigParser()
    KEYS_DIR = os.path.join(
        "C:\\Users\\paulf\\OneDrive\\Source\\Python Projects\\API_Keys"
    )
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

    GDAL_LIBRARY_PATH = r"C:\\OSGeo4W\\bin\\gdal311.dll"
    GEOS_LIBRARY_PATH = r"C:\\OSGeo4W\\bin\\geos_c.dll"
    INSTALLED_APPS += [
        "django.contrib.gis",
    ]
    engine = "django.contrib.gis.db.backends.postgis"

    db_pswd = config["MySQL"]["p"]

    # Get Other API keys
    OTAPI_APP_ID = config["opentransport"]["app_id"]
    OTAPI_API_KEY = config["opentransport"]["api_key"]

    DATABASES = {
        "default": {
            "ENGINE": engine,
            "NAME": "TPAM",
            "USER": "postgres",
            "PASSWORD": db_pswd,
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

    MAP_TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    MAP_TILE_ATTRIBUTION = "© OpenStreetMap contributors"
    MAP_TILE_SUBDOMAINS = "abc"
    MAP_TILE_PROVIDER = "osm"
    MAP_TILE_API_KEY = None
