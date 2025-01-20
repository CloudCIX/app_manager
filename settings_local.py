# Local settings that change on a per application / per environment basis
import os

PGSQLAPI_PASSWORD = os.getenv('PGSQLAPI_PASSWORD', 'pw')
PGSQLAPI_USER = os.getenv('PGSQLAPI_USER', 'postgres')
PGSQLAPI_HOST = os.getenv('PGSQLAPI_HOST', 'pgsqlapi')

POD_NAME = os.getenv('POD_NAME', 'pod')
ORGANIZATION_URL = os.getenv('ORGANIZATION_URL', 'example.com')

ALLOWED_HOSTS = (
    f'appmanager.{POD_NAME}.{ORGANIZATION_URL}',
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    'app_manager': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'app_manager',
        'USER': PGSQLAPI_USER,
        'PASSWORD': PGSQLAPI_PASSWORD,
        'HOST': PGSQLAPI_HOST,
        'PORT': '5432',
    },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_default',
        'USER': PGSQLAPI_USER,
        'PASSWORD': PGSQLAPI_PASSWORD,
        'HOST': PGSQLAPI_HOST,
        'PORT': '5432',
    },
}

DATABASE_ROUTERS = [
    'app_manager.db_router.AppManagerRouter',
]

INSTALLED_APPS = [
    'app_manager',
]

# Localisation
USE_I18N = False
USE_L10N = False

ORG = ORGANIZATION_URL.split('.')[0]
APPLICATION_NAME = os.getenv('APPLICATION_NAME', f'{POD_NAME}_{ORG}_app_manager')

CLOUDCIX_INFLUX_TAGS = {
    'service_name': APPLICATION_NAME,
}
