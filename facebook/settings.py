from pathlib import Path
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.utils import timezone as tz
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import environ
from datetime import timedelta

env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
)
environ.Env.read_env(BASE_DIR / '.env')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", cast=str, default='django-insecure-rfs-uoe-=jq7^!i*z%rf$(mnat!m@haxy&5@&h8wfy(m=ot7_!')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = env("ALLOWED_HOSTS", cast=list, default=['127.0.0.1', 'localhost'])
AUTH_USER_MODEL = 'accounts.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'common.apps.CommonConfig',
    'django_tables2',
    'crispy_forms',
    "crispy_bootstrap5",
    'django.contrib.humanize',
    'django_jalali',
    'chartjs',
    'slick_reporting',
    'market',
    "django_select2",
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_hotp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_email',
    'django_huey',
    'django_htmx',
    'formtools',
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [#this name will be used in decorators below
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_ratelimit.middleware.RatelimitMiddleware",
    'django_otp.middleware.OTPMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = 'facebook.urls'
RATELIMIT_VIEW = 'core.views.ratelimited_error'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'facebook.wsgi.application'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = env("EMAIL_HOST", cast=str, default=None)
EMAIL_PORT = env("EMAIL_PORT", cast=int, default='587')
EMAIL_HOST_USER = env("EMAIL_HOST_USER", cast=str, default=None)
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", cast=str, default=None)
EMAIL_USE_TLS = env("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_USE_SSL = env("EMAIL_USE_SSL", cast=bool, default=False)
ADMIN_USER_NAME=env("ADMIN_USER_NAME", default="admin")
ADMIN_USER_EMAIL=env("ADMIN_USER_EMAIL", default=None)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)
MANAGERS=[]
ADMINS=[]
if all([ADMIN_USER_NAME, ADMIN_USER_EMAIL]):
    ADMINS +=[
        (f'{ADMIN_USER_NAME}', f'{ADMIN_USER_EMAIL}')
    ]
    MANAGERS=ADMINS
# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SELECT2_CACHE_BACKEND = "default"
# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "ON_LOGIN_SUCCESS": "rest_framework_simplejwt.serializers.default_on_login_success",
    "ON_LOGIN_FAILED": "rest_framework_simplejwt.serializers.default_on_login_failed",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(days=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=14),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",

    "CHECK_REVOKE_TOKEN": False,
    "REVOKE_TOKEN_CLAIM": "hash_password",
    "CHECK_USER_IS_ACTIVE": True,
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'staticfiles']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# SLICK_REPORTING_SETTINGS = {
#
#     "JQUERY_URL": "https://code.jquery.com/jquery-3.7.0.min.js",
#
#     "DEFAULT_START_DATE_TIME": datetime(
#         tz.now().year,
#         1,
#         1,
#         0,
#         0,
#         0,
#         tzinfo=timezone.utc
#     ),
#
#     "DEFAULT_END_DATE_TIME": tz.now(),
#     "DEFAULT_CHARTS_ENGINE": 'chartsjs',
#
#     "MEDIA": {
#
#         "override": False,
#
#         "js": (
#
#             "https://cdn.jsdelivr.net/momentjs/latest/moment.min.js",
#
#             "https://cdn.datatables.net/1.13.4/js/jquery.dataTables.min.js",
#
#             "https://cdn.datatables.net/1.13.4/js/dataTables.bootstrap5.min.js",
#
#             "slick_reporting/slick_reporting.js",
#
#             "slick_reporting/slick_reporting.report_loader.js",
#
#             "slick_reporting/slick_reporting.datatable.js",
#         ),
#
#         "css": {
#
#             "all": (
#
#                 "https://cdn.datatables.net/1.13.4/css/dataTables.bootstrap5.min.css",
#
#             ),
#         },
#     },
#
#     "FONT_AWESOME": {
#
#         "CSS_URL": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css",
#
#         "ICONS": {
#
#             "pie": "fas fa-chart-pie",
#
#             "bar": "fas fa-chart-bar",
#
#             "line": "fas fa-chart-line",
#
#             "area": "fas fa-chart-area",
#
#             "column": "fas fa-cahrt-bar",
#         },
#     },

#     "CHARTS": {
#
#         "highcharts": "$.slick_reporting.highcharts.displayChart",
#
#         "chartjs": "$.slick_reporting.chartjs.displayChart",
#     },
#
# "MESSAGES": {
#     "total": "Total",
#     "export_to_csv": "Export CSV",
#     "print_report": "Print Report",
# },
# }
SLICK_REPORTING_SETTINGS = {
    "JQUERY_URL": "https://code.jquery.com/jquery-3.7.0.min.js",
}

DJANGO_HUEY = {
    'default': 'first',
    'queues': {
        'first': {
            'huey_class': 'huey.RedisHuey',
            'name': 'first_tasks',
            'consumer': {
                'workers': 3,
                'worker_type': 'thread',
            },
        },
        'emails': {
            'huey_class': 'huey.RedisHuey',
            'name': 'emails_tasks',
            'consumer': {
                'workers': 2,
                'worker_type': 'thread',
            },
        }
    }
}
