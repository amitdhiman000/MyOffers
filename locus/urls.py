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
    path('', views.home_view, name='home_view'),
    path('address/', views.address_view, name='address_view'),
    path('address/create/', views.address_create, name='address_create'),
    path('address/update/', views.address_update, name='address_update'),
    path('address/patch/', views.address_patch, name='address_patch'),
    path('address/delete/', views.address_delete, name='address_delete'),
]
