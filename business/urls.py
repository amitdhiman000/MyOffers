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
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.business_home_view, name='business_home_view'),
	url(r'^create/$', views.business_create, name='business_create'),
	url(r'^update/$', views.business_update, name='business_update'),
    url(r'^delete/$', views.business_delete, name='business_delete'),
	url(r'^address-create/$', views.business_address_create, name='business_address_create'),
	url(r'^address-update/$', views.business_address_update, name='business_address_update'),
	url(r'^address-delete/$', views.business_address_delete, name='business_address_delete'),
]
