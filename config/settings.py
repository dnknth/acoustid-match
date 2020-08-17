# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

import os

env = os.environ.get

BASE_DIR = os.path.dirname( os.path.dirname(__file__))

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('USER'),
        'USER': env('USER'),
    },
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-(3t3!qt2egxkeb!)@wo55=a&jaejos%dfl-shb59g4b1jr+_^'


STATIC_URL = '/static/'
STATICFILES_DIRS = os.path.join( BASE_DIR, 'config', 'static'),

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join( BASE_DIR, 'media')

INTERNAL_IPS = ('127.0.0.1', )

MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'config.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    
    # Helpers
    'debug_toolbar',
    
    # Apps
    'fingerprints',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (
            os.path.join( BASE_DIR, 'config', 'templates'),
        ),
        
        'OPTIONS':{
            'context_processors': (
                'django.template.context_processors.request',
            	'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
            	'django.contrib.messages.context_processors.messages',
            ),
            'debug': DEBUG,
        }
    },
]

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    # 'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.timer.TimerPanel',
)

#### Auth
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

#### AcoustID
ACOUSTID_API_KEY = env( 'ACOUSTID_API_KEY')
AUDIO_FORMATS = ('aac', 'aif', 'flac', 'm4a', 'mp3', 'wav')
FINGERPRINT_VERSION = 1

# minimum similarity with the worst matching fingerprint
TRACK_GROUP_MERGE_THRESHOLD = 0.4

# maximum alignment differences of fingerprints in a track
TRACK_MAX_OFFSET = 80

FINGERPRINT_MAX_LENGTH_DIFF = 7

del( env)
