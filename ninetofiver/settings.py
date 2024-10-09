import ldap
import os
import yaml

from configurations import Configuration, values
from django_auth_ldap.config import LDAPSearch
from django_auth_ldap.config import LDAPSearchUnion
from ninetofiver.utils import get_django_environment

CFG_FILE_PATH = os.path.expanduser(os.environ.get('CFG_FILE_PATH', '/etc/925r/config.yml'))


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENVIRONMENT = get_django_environment()


class Base(Configuration):
    """Base configuration."""
    
    @classmethod
    def pre_setup(cls):
        super(Base, cls).pre_setup()
        cls._load_cfg_file()
        cls._process_cfg()

    @classmethod
    def _load_cfg_file(cls):
        data = None

        try:
            with open(CFG_FILE_PATH, 'r') as f:
                # https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation
                data = yaml.safe_load(f)
        except BaseException:
            pass

        if data:
            for key, value in data.items():
                setattr(cls, key, value)

    @classmethod
    def _process_cfg(cls):
        cls.AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
            *[LDAPSearch(x[0], getattr(ldap, x[1]), x[2]) for x in cls.AUTH_LDAP_USER_SEARCHES]
        )

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '$6_rj^w8_*ihrkohpckeq4028ai1*no1cw1vp*2%oe8+#gp1sj'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = False

    ALLOWED_HOSTS = ['localhost']

    # Apps included here will be included
    # in the test suite
    NINETOFIVER_APPS = [
        'ninetofiver',
        'ninetofiver.api_v2'
    ]

    # Application definition
    INSTALLED_APPS = [
        'whitenoise.runserver_nostatic',
    ] + NINETOFIVER_APPS + [
        # deprecated in django 2.0, replaced by django_select2
        # 'django_admin_select2',
        'dal',
        'crispy_bootstrap4',
        'dal_select2',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'rest_framework_swagger',
        'django_filters',
        'rest_framework_filters',
        'corsheaders',
        'polymorphic',
        'oauth2_provider',
        'crispy_forms',
        'django_gravatar',
        'django_countries',
        'rangefilter',
        'django_admin_listfilter_dropdown',
        'admin_auto_filters',
        'silk',
        'wkhtmltopdf',
        'django_tables2',
        'django_select2',
        'phonenumber_field',
        'import_export',
        'adminsortable',
        'logentry_admin',
        'recurrence',
        'django_minio_backend',
        'django_minio_backend.apps.DjangoMinioBackendConfig',
        'storages',
    ]

    MIDDLEWARE = [
        'silk.middleware.SilkyMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'ninetofiver.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            # 'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django_settings_export.settings_export',
                ],
                'loaders': [
                    ('pypugjs.ext.django.Loader', (
                        'apptemplates.Loader',
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    )),
                ],
                'builtins': ['pypugjs.ext.django.templatetags'],
            },
        },
    ]

    WSGI_APPLICATION = 'ninetofiver.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.10/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'HOST': os.getenv('MYSQL_HOST', 'mysql.{env}.925r.local'.format(env=ENVIRONMENT)),
            'PORT': os.getenv('MYSQL_PORT', '3306'),
            'NAME': os.getenv('MYSQL_DATABASE', 'ninetofiver'),
            'USER': os.getenv('MYSQL_USER', 'ninetofiver'),
            'PASSWORD': os.getenv('MYSQL_PASSWORD', ''),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            'CONN_MAX_AGE': 600,
        },
    }

    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

    # Password validation
    # https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/1.10/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.10/howto/static-files/
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    STATIC_URL = '/static/'
    # User-uploaded files
    MEDIA_ROOT = values.Value(os.path.join(BASE_DIR, 'media/'))
    MEDIA_URL = '/media/'
    # Auth
    LOGIN_URL = 'login'
    LOGOUT_URL = 'logout'

    # REST framework
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
            'ninetofiver.authentication.ApiKeyAuthentication',
        ),
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ),
        'DEFAULT_FILTER_BACKENDS': (
            'django_filters.rest_framework.DjangoFilterBackend',
        ),
        'EXCEPTION_HANDLER': 'ninetofiver.exceptions.exception_handler',
        'TEST_REQUEST_DEFAULT_FORMAT': 'json',
        'DEFAULT_PAGINATION_CLASS': 'ninetofiver.pagination.CustomizablePageNumberPagination',
        'PAGE_SIZE': 25,
    }

    # Swagger
    SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            # 'basic': {
            #     'type': 'basic'
            # },
            # 'primary': {
            #     'type': 'oauth2',
            #     'flow': 'implicit',
            #     'tokenUrl': '/oauth/v2/token',
            #     'authorizationUrl': '/oauth/v2/authorize',
            #     'scopes': {
            #         'write': 'Write data',
            #         'read': 'Read data',
            #     }
            # },
        },
        'DOC_EXPANSION': 'list',
        'SHOW_REQUEST_HEADERS': True,
        'JSON_EDITOR': False,
        # 'APIS_SORTER': 'alpha',
        # 'OPERATIONS_SORTER': 'method',
        'VALIDATOR_URL': None,
    }

    # Profiling
    SILKY_AUTHENTICATION = True  # User must login
    SILKY_AUTHORISATION = True  # User must have permissions
    SILKY_MAX_REQUEST_BODY_SIZE = 0
    SILKY_MAX_RESPONSE_BODY_SIZE = 0
    SILKY_META = True
    SILKY_MAX_RECORDED_REQUESTS = 1000
    SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 1
    SILKY_INTERCEPT_PERCENT = 5

    # Crispy forms
    CRISPY_TEMPLATE_PACK = 'bootstrap4'

    # Gravatar
    GRAVATAR_DEFAULT_IMAGE = 'identicon'

    # Registration
    ACCOUNT_ACTIVATION_DAYS = 7
    REGISTRATION_OPEN = False

    # CORS
    CORS_ORIGIN_ALLOW_ALL = True

    # Exported settings available in templates
    SETTINGS_EXPORT = [
        'DEBUG',
        'REGISTRATION_OPEN',
        'BASE_URL',
    ]

    # Authentication using LDAP
    AUTHENTICATION_BACKENDS = [
        'django_auth_ldap.backend.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]

    AUTH_LDAP_SERVER_URI = "ldap://ldap"
    AUTH_LDAP_START_TLS = False
    AUTH_LDAP_BIND_DN = "cn=admin,dc=example,dc=org"
    AUTH_LDAP_BIND_PASSWORD = "admin"
    AUTH_LDAP_USER_SEARCHES = [
        ['dc=example,dc=org', 'SCOPE_SUBTREE', '(cn=%(user)s)'],
    ]
    AUTH_LDAP_USER_ATTR_MAP = {
        'email': 'mail',
        'first_name': 'givenName',
        'last_name': 'sn',
    }
    AUTH_LDAP_ALWAYS_UPDATE_USER = True
    AUTH_LDAP_GLOBAL_OPTIONS = {
        ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_ALLOW,
    }

    # PDFs
    WKHTMLTOPDF_CMD_OPTIONS = {
        'encoding': 'utf8',
        'quiet': True,
        'margin-bottom': '10mm',
        'margin-left': '5mm',
        'margin-right': '5mm',
        'margin-top': '10mm',
    }

    # REDMINE
    REDMINE_URL = values.Value(None)
    REDMINE_API_KEY = values.Value(None)
    REDMINE_ISSUE_CONTRACT_FIELD = values.Value('925r_contract')

    EMAIL_HOST = values.Value('localhost')
    EMAIL_PORT = values.Value(25)
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    DEFAULT_FROM_EMAIL = values.Value('noreply@example.org')

    # Absolute URL generation without request info
    BASE_URL = values.Value('http://localhost:8000')
    # Default starting hour for working days
    DEFAULT_WORKING_DAY_STARTING_HOUR = 9

    # Mattermost integration
    MATTERMOST_INCOMING_WEBHOOK_URL = values.Value(None)
    MATTERMOST_PERFORMANCE_REMINDER_NOTIFICATION_ENABLED = values.Value(True)
    MATTERMOST_TIMESHEET_REMINDER_NOTIFICATION_ENABLED = values.Value(True)

    # Rocketchat integration
    ROCKETCHAT_INCOMING_WEBHOOK_URL = values.Value(None)
    ROCKETCHAT_PERFORMANCE_REMINDER_NOTIFICATION_ENABLED = values.Value(True)
    ROCKETCHAT_TIMESHEET_REMINDER_NOTIFICATION_ENABLED = values.Value(True)

    # MinIO settings
    MINIO_CONSISTENCY_CHECK_ON_START = True
    MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT', 'minio:9000')
    MINIO_USE_HTTPS = False

    MINIO_PUBLIC_BUCKETS  = ["ninetofiver"]
    MINIO_MEDIA_FILES_BUCKET = os.environ.get('MINIO_MEDIA_FILES_BUCKET', 'ninetofiver')
    MINIO_AUTO_CREATE_MEDIA_BUCKET = True
    DEFAULT_FILE_STORAGE = 'django_minio_backend.models.MinioBackend'

    STORAGES = {
        "default": {
            "BACKEND": 'django_minio_backend.models.MinioBackend',
            "OPTIONS": {
                'access_key': os.getenv('MINIO_ACCESS_KEY', 'svcaccesskey'),
                'secret_key': os.getenv('MINIO_SECRET_KEY', 'svcsecretkey'),
                'bucket_name': os.getenv('MINIO_MEDIA_FILES_BUCKET', 'ninetofiver'),
                'endpoint': os.getenv('MINIO_ENDPOINT', 'minio:9000'),
                'secure': False,
                'region_name': 'us-east-1',
            },
        },
    }

    MINIO_MEDIA_FILES_BUCKET = os.environ.get('MINIO_MEDIA_FILES_BUCKET', 'ninetofiver')
    MEDIA_URL = os.getenv('MINIO_MEDIA_URL', 'http://minio:9000/ninetofiver/')






class Dev(Base):
    """Dev configuration."""

    # INSTALLED_APPS = ['debug_toolbar'] + Base.INSTALLED_APPS
    # MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + Base.MIDDLEWARE

    # for 'debug_toolbar'
    # DEBUG_TOOLBAR_CONFIG = {
    #     'RESULTS_CACHE_SIZE': 150,  # to see more SQL queries
    # }

    DEBUG = True

    ALLOWED_HOSTS = ['*']

    # Database
    # https://docs.djangoproject.com/en/1.10/ref/settings/#databases
    DEFAULT_FILE_STORAGE = 'django_minio_backend.models.MinioBackend'
    DATABASES = {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'HOST': os.getenv('MYSQL_HOST', 'mysql'),
            'PORT': os.getenv('MYSQL_PORT', '3306'),
            'NAME': os.getenv('MYSQL_DATABASE', 'ninetofiver'),
            'USER': os.getenv('MYSQL_USER', 'ninetofiver'),
            'PASSWORD': os.getenv('MYSQL_PASSWORD', 'ninetofiver'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
            'CONN_MAX_AGE': 600,
        },
    }

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     }
    # }

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'handlers': {
            'syslog': {
                'class': 'logging.handlers.SysLogHandler',
                'formatter': 'verbose',
                'facility': 'user',
            },
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        'loggers': {
            'ninetofiver': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        }
    }

    INTERNAL_IPS = Base.INTERNAL_IPS + [
        '127.0.0.1',
    ]

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

    # Profiling
    SILKY_INTERCEPT_PERCENT = 100

    REGISTRATION_OPEN = True
    
    # EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


class Prod(Base):
    """Prod configuration."""

    # Logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        }
    }


class Stag(Prod):
    """Stag configuration."""
