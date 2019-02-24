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
from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('locus/<path:query>', views.locus_view, name='locus_view'),
	path('locus-add/<path:query>', views.locus_add_view, name='locus_add_view'),
	path('locus-auth/<path:query>', views.locus_auth, name='locus_auth'),
	path('categories/<path:query>', views.category_view, name='category_view'),
	path('category-add/<path:query>', views.category_add_view, name='category_add_view'),
	path('category-auth/<path:query>', views.locus_auth, name='locus_auth'),
	path('messages/', views.messages_view, name='messages_view'),
]
