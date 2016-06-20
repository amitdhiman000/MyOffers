from landcrab.settings.base import *
import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = False

# Parse database configuration from $DATABASE_URL
DATABASES['default'] = dj_database_url.config()
# DATABASES['default'] =  dj_database_url.config(default='postgres://user:pass@localhost/dbname')
# DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'
# DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}
# DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']
