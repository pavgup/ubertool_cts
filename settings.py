"""
Django settings for UberDjango project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import secret

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Define ENVIRONMENTAL VARIABLES for project (replaces the app.yaml)
os.environ.update({
    'UBERTOOL_BATCH_SERVER': 'http://uberrest-topknotmeadows.rhcloud.com/',
    'UBERTOOL_MONGO_SERVER': 'http://uberrest-topknotmeadows.rhcloud.com',
    'UBERTOOL_SECURE_SERVER': 'http://uberrest-topknotmeadows.rhcloud.com',
    # 'UBERTOOL_REST_SERVER': 'http://localhost:80',
    'UBERTOOL_REST_SERVER': 'http://54.83.18.251:80',
    'CTS_JCHEM_SERVER': 'http://134.67.114.2',
    'CTS_TEST_SERVER': 'http://134.67.114.6', # test rest server (internal)
    # 'CTS_TEST_SERVER': 'http://172.20.100.16', # test rest server (internal)
    'PROJECT_PATH': PROJECT_ROOT,
})

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secret.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []

APPEND_SLASH = True

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates').replace('\\','/'),

)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'docs'
    'filters',
    # 'templatetags.my_filter'
    'test_cts' # Pavan added this for the TEST suite CTS app.  Not to be confused with any other test software.
)

# This breaks the pattern of a "pluggable" TEST_CTS django app, but it also makes it convenient to describe the server hosting the TEST API.
TEST_CTS_PROXY_URL = "http://10.0.2.2:7080/"

MIDDLEWARE_CLASSES = (
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi_local.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Setups databse-less test runner (Only needed for running test)
TEST_RUNNER = 'testing.DatabaselessTestRunner'

# CACHE Setup - required to run Django "sessions" without a database

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATIC_URL = '/static/'

# print 'BASE_DIR = %s' %BASE_DIR
# print 'PROJECT_ROOT = %s' %PROJECT_ROOT

# Path to Sphinx HTML Docs
# http://django-docs.readthedocs.org/en/latest/

DOCS_ROOT = os.path.join(PROJECT_ROOT, 'docs', '_build', 'html')

DOCS_ACCESS = 'public'

if DEBUG:
   import logging
   logging.basicConfig(
       level = logging.DEBUG,
       format = '%(asctime)s %(levelname)s %(message)s',
   )
