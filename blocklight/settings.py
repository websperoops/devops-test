from celery.schedules import crontab
from datetime import timedelta
from django.contrib.messages import constants as messages
import netifaces
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWED_HOSTS = ['68.183.20.242', '206.189.238.123', '142.93.120.127', '0.0.0.0',
                 'dev.blocklight.io', '127.0.0.1', 'localhost', '.blocklight.io',
                 'www.blocklight.io', '.google.com', '.mailchimp.com', '.intuit.com',
                 '.facebook.com', '.instagram.com', '.shipstation.com', '.shopify.com', 'testserver']

DEBUG = os.environ.get('DEBUG', "").lower() == 'true'
DJANGO_DEBUG = os.environ.get('DJANGO_DEBUG', "").lower() == 'true'

LOG_FILE = os.path.join(BASE_DIR, 'log')
print(LOG_FILE)
LOG_FILE_MAX_SIZE = 15728640  # 15Mb
LOG_BACKUP_COUNT = 10

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'sql_mode': 'traditional',
            "init_command": "SET NAMES utf8mb4 COLLATE utf8mb4_bin;",
            "charset": "utf8mb4"
        },
        'NAME': os.environ['MYSQL_DB_NAME'],
        'USER': os.environ['MYSQL_DB_USER'],
        'PASSWORD': os.environ['MYSQL_DB_PASSWORD'],
        'HOST': os.environ['MYSQL_DB_HOST'],
        'PORT': int(os.environ['MYSQL_DB_PORT']),
    }
}

CACHE_BACKEND = os.environ['CACHE_BACKEND']
CACHES = {'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache', }, }
CACHE_MIDDLEWARE_SECONDS = 1800
SITE_NAME = os.environ['SITE_NAME']
SITE_DOMAIN = os.environ['SITE_DOMAIN']

# GOOGLE SETTINGS

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
GOOGLE_SCOPES = os.environ['GOOGLE_SCOPES']
# DEFINE ENV - GLOBAL
INSTALLED_APPS = [
    'dal',  # django-autocomplete-light
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.syndication',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'werkzeug_debugger_runserver',
    'hijack',
    'compat',
    'plus',
    'django_extensions',
    'django_smtp_ssl',
    # 'compressor',
    'reset_migrations',
    'celery',
    'avatar',
    'regex',
    'invitations',
    'layout',
    'dashboards',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.shopify',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.quickbooks',
    'allauth.socialaccount.providers.mailchimp',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.etsy',
    'allauth.socialaccount.providers.woocommerce',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.routable_page',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'modelcluster',
    'taggit',
    'django_nose',
    'rest_framework',
    'django_filters',
    'blocklight',
    'easy_thumbnails',
    'mptt',
    'payments_router',
    'stripe_payments',
    'shopify_payments',
    'user_tiers',
    'blocklight_api'
]
# INSTALLED_APPS += ("djcelery", )

ROOT_URLCONF = 'blocklight.urls'
WSGI_APPLICATION = 'blocklight.wsgi.application'
SITE_ID = 1  # Change to 1 for localhost
LOGIN_REDIRECT_URL = '/router/'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'user_tiers.middleware.TiersMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.contrib.legacy.sitemiddleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'dashboards/templates'),
            os.path.join(BASE_DIR, 'layout/templates'),
            os.path.join(BASE_DIR, 'layout/templates/allauth'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

WAGTAIL_SITE_NAME = os.environ['WAGTAIL_SITE_NAME']

# AllAuth Profile Configs
ACCOUNT_FORMS = {'signup': 'dashboards.forms.BetaSignupForm'}
# Security
# SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
# X_FRAME_OPTIONS = 'DENY'
# SESSION_COOKIE_HTTPONLY = True
# SESSION_COOKIE_SECURE = False
# X_FRAME_OPTIONS = 'DENY'

SECRET_KEY = os.environ['SECRET_KEY']

# Stripe
STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_ENDPOINT_SECRET = os.environ['STRIPE_ENDPOINT_SECRET']

# Shopify
SHOPIFY_API_VERSION = os.environ['SHOPIFY_API_VERSION']
SHOPIFY_TEST_MODE = bool(os.environ['SHOPIFY_API_VERSION'])

# EMAIL CONFIGS
SOCIALACCOUNT_QUERY_EMAIL = os.environ['SOCIALACCOUNT_QUERY_EMAIL'].lower(
) == 'true'
EMAIL_BACKEND = os.environ['EMAIL_BACKEND']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_HOST = os.environ['EMAIL_HOST']
SERVER_EMAIL = os.environ['SERVER_EMAIL']
SMTP_ENABLED = os.environ['SMTP_ENABLED']
EMAIL_USE_SSL = os.environ['EMAIL_USE_SSL']
EMAIL_PORT = os.environ['EMAIL_PORT']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']

# MAILCHIMP SUBSCRIPTION CONFIGS FOR NEW SIGNUPS
MAILCHIMP_API_KEY = os.environ['MAILCHIMP_API_KEY']
MAILCHIMP_EMAIL_ID = os.environ['MAILCHIMP_EMAIL_ID']
SIGNUP_MAIL_LIST_ID = os.environ['SIGNUP_MAIL_LIST_ID']
SIGNUP_LIST_NAME = os.environ['SIGNUP_LIST_NAME']

# NEWSLETTER LIST ID
NEWSLETTER_LIST_ID = os.environ['NEWSLETTER_LIST_ID']
NEWSLETTER_LIST_NAME = os.environ['NEWSLETTER_LIST_NAME']

# ADMIN EMAIL TO WHICH DEFAULT PASSWORD AND BUSINESS DETAILS ARE SENT TO
SIGNUP_ADMIN_EMAIL = os.environ['SIGNUP_ADMIN_EMAIL']
# MAILCHIMP_LIST_ID = 1

ACCOUNT_DEFAULT_HTTP_PROTOCOL = os.environ['ACCOUNT_DEFAULT_HTTP_PROTOCOL']
ACCOUNT_AUTHENTICATION_METHOD = os.environ['ACCOUNT_AUTHENTICATION_METHOD']
ACCOUNT_EMAIL_REQUIRED = os.environ['ACCOUNT_EMAIL_REQUIRED'].lower() == 'true'
ACCOUNT_UNIQUE_EMAIL = os.environ['ACCOUNT_UNIQUE_EMAIL'].lower() == 'true'
ACCOUNT_UNIQUE_USERNAME = os.environ['ACCOUNT_UNIQUE_USERNAME'].lower(
) == 'true'
ACCOUNT_USERNAME_REQUIRED = os.environ['ACCOUNT_USERNAME_REQUIRED'].lower(
) == 'true'
ACCOUNT_LOGOUT_ON_GET = os.environ['ACCOUNT_LOGOUT_ON_GET'].lower() == 'true'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = int(os.environ['ACCOUNT_LOGIN_ATTEMPTS_LIMIT'])
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
SOCIALACCOUNT_QUERY_EMAIL = os.environ['SOCIALACCOUNT_QUERY_EMAIL'].lower(
) == 'true'

# SOCIAL_AUTH_FACEBOOK_KEY = '285401232146621'  # App ID
# SOCIAL_AUTH_FACEBOOK_SECRET = '3f0db6d8f6372aeb4a706a7f4997dae6'  # App Secret

# EMAIL_USE_TLS = True
# # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# # EMAIL_USE_SSL = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER    = 'info@blocklight.io'
# EMAIL_HOST_PASSWORD = 'Blocklight13$'
# #EMAIL_PORT = 465
# EMAIL_PORT = 587

# ### Email Testing -- Prints to Console ####
# EMAIL_BACKEND ='django.core.mail.backends.console.EmailBackend'
# DEFAULT_FROM_EMAIL = 'testing@example.com'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = False
# EMAIL_PORT = 1025

# HIJACK CONFIGS
HIJACK_LOGIN_REDIRECT_URL = os.environ['HIJACK_LOGIN_REDIRECT_URL']
HIJACK_LOGOUT_REDIRECT_URL = os.environ['HIJACK_LOGOUT_REDIRECT_URL']
HIJACK_USE_BOOTSTRAP = os.environ['HIJACK_USE_BOOTSTRAP'].lower() == 'true'
HIJACK_ALLOW_GET_REQUESTS = os.environ['HIJACK_ALLOW_GET_REQUESTS'].lower(
) == 'true'
HIJACK_AUTHORIZE_STAFF = os.environ['HIJACK_AUTHORIZE_STAFF'].lower() == 'true'

# Timezone & Language
LANGUAGE_CODE = os.environ['LANGUAGE_CODE']
TIME_ZONE = os.environ['TIME_ZONE']
USE_I18N = True
USE_L10N = True
USE_TZ = True
PARLER_DEFAULT_LANGUAGE_CODE = 'en'
PARLER_LANGUAGES = {
    None: (
        {'code': 'en', },
        {'code': 'en-us', },
        {'code': 'it', },
        {'code': 'nl', },
    ),
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,
    }
}


def get_host_url():
    urls = {
        'localhost': r'https://127.0.0.1:8000',
        'development': r'https://dev.blocklight.io/',
        'production': r'https://blocklight.io/'
    }
    return urls[os.environ['ENVIRONMENT']]


SOCIALACCOUNT_PROVIDERS = {
    'shopify': {
        'SCOPE': [
            "read_all_orders",
            'read_orders',
            'read_products',
            'read_reports',
            'read_shipping',
            'read_inventory',
            'read_customers',
            'read_analytics',
            'read_draft_orders',
            'read_product_listings',
            'read_price_rules',
            'read_content',
            'read_fulfillments'
        ],
    },
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': [
            'email',  # approved
            'public_profile',  # approved
            # 'user_friends',  # approved
            # 'user_gender',  # approved
            # 'pages_manage_cta',  # denied
            'instagram_basic',
            'instagram_manage_insights',
            # 'read_audience_network_insights',
            # 'instagram_manage_comments',
            # 'leads_retrieval',
            'read_insights',
            # 'ads_read',
            # 'pages_manage_instant_articles',
            # 'pages_messaging',
            # 'pages_messaging_phone_number',
            # 'user_events',
            # 'user_age_range',

            # 'pages_messaging_subscriptions',
            'pages_show_list',
            # 'publish_pages',
            # 'read_page_mailboxes',
            # 'user_posts',
            # 'user_tagged_places',
            # 'user_videos',
            # 'pages_manage_ads',
            # 'pages_manage_metadata',
            'pages_read_engagement',
            'pages_read_user_content'
        ],
        'INIT_PARAMS': {'cookie': True},
        'VERIFIED_EMAIL': False,
    },
    'instagram':
        {
            # 'SCOPE': [
            #     # 'instagram_basics',
            #     # 'instagram_manage_insights',
            #     # 'manage_pages',
            # ],
            'AUTH_PARAMS': {
                'access_type': 'online',
            }
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
            # 'https://www.googleapis.com/auth/analytics',
            # 'https://www.googleapis.com/auth/analytics.edit',
            'https://www.googleapis.com/auth/analytics.readonly'
            # 'ga-dev-tools.appspot.com'
        ],
        'AUTH_PARAMS': {

            'access_type': 'offline',
            'approval_prompt': 'force'
        },
        'PROMPT': ['select_account', 'consent']
    },
    'quickbooks': {
        'SANDBOX': True,
        'SCOPE': [
            'openid',
            'com.intuit.quickbooks.accounting com.intuit.quickbooks.payment',
            'profile',
            'phone',
        ]
    },

    # 'twitter': {


    #         'APP': {
    #             'client_id': 'Y496hWM2BRWIKws1QqA0Mub9z',
    #             'secret': '8vcgPa8yUdsVtk1YaAEWlCLdWC2QYP7gWzbnk7lAkQ75AMAdl1',
    #             'key': ''
    #         }
    # },

    "etsy": {

        'SCOPE': ["email_r", "listings_r", "transactions_r",
                  "billing_r", "profile_r",
                  "address_r", "feedback_r", "treasury_r", ]
    },
    "woocommerce": {
        'SCOPE': [],
        'AUTH_PARAMS': {
            'app_name': "blocklight",
            'user_id': 1,
            'scope': 'read',
            'return_url': f'{get_host_url()}/dashboards/integrations/',
            'callback_url': f'{get_host_url()}/woocommerce/login/callback'
        }
    }
}

# Configure Error Logging on Server
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
        'custom': {
            'format': '%(asctime)s %(levelname)-8s %(name)-10s [%(filename)s].[%(funcName)s]: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': LOG_FILE_MAX_SIZE,
            'backupCount': LOG_BACKUP_COUNT,
            'formatter': 'custom'
        },
        'email': {
            'class': 'logging.handlers.SMTPHandler',
            'formatter': 'custom',
            'mailhost': 'smtp.gmail.com',
            'fromaddr': 'beta@blocklight.io',
            'toaddrs': 'beta@blocklight.io',
            'credentials': ("beta@blocklight.io", "Test_4_success"),
            'subject': 'logs',
            'secure': (),
            'level': 'ERROR'
        },
        # 'null': {
        #     'class': 'logging.NullHandler'
        # }
    },
    'loggers': {
        # '': {
        #     'handlers': ['null', 'email'],
        # },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'WARNING' if not DJANGO_DEBUG else 'DEBUG',
            'propagate': True,
        },
        'dashboards': {
            'handlers': ['file', 'console'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['file', 'console'],
            'level': 'INFO' if not DEBUG else 'DEBUG',
            'propagate': True,
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# Find out what the IP addresses are at run time
# Otherwise Gunicorn will reject the connections


def ip_addresses():
    ip_list = []
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        for x in (netifaces.AF_INET, netifaces.AF_INET6):
            if x in addrs:
                ip_list.append(addrs[x][0]['addr'])
    return ip_list


ALLOWED_HOSTS += ip_addresses()

# Import Celery Last

# djcelery.setup_loader()
CELERY_BROKER_URL = os.environ['CELERY_BROKER_URL']
CELERY_RESULT_BACKEND = os.environ['CELERY_RESULT_BACKEND']
CELERY_RESULT_PERSISTENT = os.environ['CELERY_RESULT_PERSISTENT'].lower(
) == 'true'
CELERY_TIMEZONE = os.environ['CELERY_TIMEZONE']
CELERY_ACCEPT_CONTENT = ['pickle', 'json']
CELERY_TASK_SERIALIZER = 'pickle'

# CELERY_ALWAYS_EAGER = True  # This will supress asynchronous behaviour of tasks (good for testing)

# Note: this is a way to set periodic tasks in celery=3.1.x. It's changed in a latest versions.
CELERYBEAT_SCHEDULE = {
    'run-sync-every-15-minutes': {
        'task': 'sync_all_integrations_data',
        'schedule': timedelta(seconds=60*15),
    },
    'consolidate-timeline-head': {
        'task': 'consolidate_timeline_head',
        'schedule': timedelta(seconds=60*20),
    },
    'consolidate-timeline': {
        'task': 'consolidate_full_timeline',
        'schedule': timedelta(hours=6, minutes=30),
    },
    'run-fb-ig-sync-every-6-hours': {
        'task': 'sync_all_fb_ig_data',
        'schedule': timedelta(hours=6),
    },
    'run-tier-payments-every-day-at-8pm': {
        'task': 'execute_all_recurring_payments',
        'schedule': crontab(minute=0, hour=20),
    },
    'run-mailchimp-delete-every-day-at-4am': {
        'task': 'delete_mailchimp_user_data_task',
        'schedule': crontab(minute=55, hour=3),
    },
    'run-trial-ending-emails-every-day-at-3pm': {
        'task': 'send_trial_ending_emails',
        'schedule': crontab(minute=0, hour=15),
    },
    'run-birthday-emails-every-day-at-3pm': {
        'task': 'send_birthday_email',
        'schedule': crontab(minute=0, hour=15),
    },
    'run-onboarding-emails-every-day-at-3pm': {
        'task': 'send_onboarding_email',
        'schedule': crontab(minute=0, hour=15),
    },
}
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Google reCAPTCHA Details
GOOGLE_RECAPTCHA_SITE_KEY = os.environ['GOOGLE_RECAPTCHA_SITE_KEY']
GOOGLE_RECAPTCHA_SECRET_KEY = os.environ['GOOGLE_RECAPTCHA_SECRET_KEY']

# Mixpanel Keys
MIXPANEL_TOKEN = os.environ['MIXPANEL_TOKEN']
MIXPANEL_SECRET = os.environ['MIXPANEL_SECRET']
