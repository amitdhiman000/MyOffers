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
	url(r'^$', views.offer_home_view, name='offer_home_view'),
	url(r'^create-new/$', views.offer_create_view, name='offer_create_view'),
	url(r'^create-new/auth/$', views.offer_create, name='offer_create'),
	url(r'^online/$', views.online_view, name='online_view'),
	url(r'^nearby/$', views.nearby_view, name='nearby_view'),
	url(r'^bulk/$', views.bulk_view, name='bulk_view'),
	url(r'^food/$', views.food_view, name='food_view'),
	#url('^(?P<offer_id>\w{0,50})/$', views.offer_detail_view, name='offer_detail_view'),
	url(r'^(?P<slug>[\w-]+)/$', views.offer_detail_view1, name="offer_detail_view1"),
]
