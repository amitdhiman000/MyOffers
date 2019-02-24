"""MyOffers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views

urlpatterns = [
    path('v1/token/create/', views.token_create),
    path('v1/token/refresh/', views.token_refresh),
    # path('v1/business/', include('business.urls_a')),
    path('v1/locus/', include('locus.urlsa')),
    # path('v1/offer/', include('offer.urls_a')),
    # path('v1/search/', include('search.urls_a')),
    # path('v1/upload/', include('upload.urls_a')),
    path('v1/user/', include('user.urlsa')),
]
