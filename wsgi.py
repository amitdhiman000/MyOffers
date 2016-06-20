import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyOffers.settings.production") #Edited by me

from django.core.wsgi import get_wsgi_application

#Added by me for Heroku
try:
    from dj_static import Cling
    application = Cling(get_wsgi_application())
except:
    application = get_wsgi_application()
