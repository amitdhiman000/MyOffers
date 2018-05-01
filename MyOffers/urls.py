"""MyOffers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'', include('home.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^business/', include('business.urls')),
    url(r'^error/', include('error.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^locus/', include('locus.urls')),
    url(r'^offer/', include('offer.urls')),
    url(r'^public/', include('public.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^upload/', include('upload.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^myadmin/', include('myadmin.urls')),
    # url(r'^admin/', admin.site.urls),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
