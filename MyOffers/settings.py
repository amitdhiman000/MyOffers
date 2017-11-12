"""
Django settings for MyOffers project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!#byfsfle(0g6q^+s12bjtw_2b+jjzxt9@)suhw7rggmu5x-ce'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# don't set this, POST request don't append slash by default
#APPEND_SLASH=False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
	#'django.contrib.admin',
	#'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'background_task',
	'ajax',
	'business',
	'error',
	'home',
	'locus',
	'offer',
	'public',
	'search',
	'upload',
	'user',
	'myadmin',
	'MyOffers',
]

MIDDLEWARE_CLASSES = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	#'django.contrib.auth.middleware.AuthenticationMiddleware',
	#'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'user.middleware.AuthMiddleware', # custom middleware
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MyOffers.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ['templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				#'django.contrib.auth.context_processors.auth',
				'django.template.context_processors.media',
				'django.contrib.messages.context_processors.messages',
				'common.context_processors.user',
				'common.context_processors.ajax',
			],
			#'string_if_invalid': '',
		},
	},
]

WSGI_APPLICATION = 'MyOffers.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'devel.sqlite3')
	}
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

import sys
## website logging settings.
LOGGING = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s:%(funcName)s(%(lineno)d) %(message)s'
        },
		'normal': {
            'format': '%(asctime)s %(levelname)s %(filename)s:%(funcName)s :(%(lineno)d) %(message)s'
        },
		'verbose': {
            'format': '%(asctime)s %(levelname)s %(pathname)s:%(funcName)s :(%(lineno)d) %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'normal',
			'stream': sys.stdout,
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/logs.log',
            'formatter': 'normal'
        },
		'file_request': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/request_logs.log',
            'formatter': 'simple'
        },
    },
    'loggers': {
		'': {
			'handlers': ['file'],
			'level': 'DEBUG',
			'propagate': True,
		},
		'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
		'django.request': {
            'handlers': ['file_request'],
            'level': 'INFO',
            'propagate': True,
        },
		'django.template': {
            'handlers': ['file_request'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] = ['console']

#AUTH_USER_MODEL = accounts.User
#AUTHENTICATION_BACKEND = (accounts.backends.UserAuth,)

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
#TIME_ZONE = 'Asia/Kolkata'
#https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'static_root')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles', 'static_dirs'),
    # '/var/www/static_files/'
]
STATIC_DATA_DIR = os.path.join(BASE_DIR, 'staticfiles', 'data')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'staticfiles', 'media_root')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_USER_FILES_DIR_NAME = 'files'
MEDIA_TMP_FILES_DIR_NAME = 'tmp'


# some custom settings
BASE_TEMPLATE = 'base_1.html'
BASE_AJAX_TEMPLATE = 'base_2.html'
DEFAULT_USER_IMAGE = 'default/user.svg'

## admin pages
##
ADMIN_LEVEL = 9
ADMIN_HOME = '/myadmin/'
ADMIN_CUSTOM_DATA = '/myadmin/fetch-custom/'
ADMIN_CUSTOM_VIEW = '/myadmin/custom-view/'

## public pages
##
PUBLIC_CONTACTS_URL = '/public/contacts/'
PUBLIC_ABOUTUS_URL = '/public/aboutus/'

## home pages
##
HOME_URL = '/'

# error urls
ERROR_ACCESS_DENIED_URL = '/error/access-denied/'
ERROR_INVALID_REQUEST_URL = '/error/invalid-request/'
ERROR_UNDER_CONSTRUCTION_URL = '/error/under-construction/'

# user pages
USER_LOGIN_NEXT = 'next'
USER_LOGIN_URL = '/user/signin/'
USER_SIGNUP_URL = '/user/signup/'
USER_SIGNUP_SUCCESS_URL = '/user/signup-success/'
USER_LOGOUT_URL = '/user/signout/'
USER_SETTING_URL = '/user/settings/'
USER_PROFILE_URL = '/user/account/'

OFFER_CREATE_NEW = '/offer/create-new/'
OFFER_CREATE_NEW_AUTH = '/offer/create-new/auth'
OFFER_CREATE_SUCCESS = '/offer/create-success/'
OFFER_CREATE_FAILURE = '/offer/create-failure/'
OFFER_DETAIL_VIEW = '/offer/detail-view/'
