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
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^locus/(?P<query>[\w\ \(\)\/]*)$', views.locus_view, name='locus_view'),
	url(r'^locus-add/(?P<query>[\w\ \(\)\/]*)$', views.locus_add_view, name='locus_add_view'),
	url(r'^locus-auth/(?P<query>[\w\ \(\)\/]*)$', views.locus_auth, name='locus_auth'),
	url(r'^categories/(?P<query>[\w\ \(\)\/\&\-]*)$', views.category_view, name='category_view'),
	url(r'^category-add/(?P<query>[\w\ \(\)\/\&\-]*)$', views.category_add_view, name='category_add_view'),
	url(r'^category-auth/(?P<query>[\w\ \(\)\/\&\-]*)$', views.locus_auth, name='locus_auth'),
	url(r'^messages/$', views.messages_view, name='messages_view'),
]
