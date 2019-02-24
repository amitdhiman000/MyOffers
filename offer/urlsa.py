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
    path('', views.offer_home_view, name='offer_home_view'),
    path('create-new/auth/', views.offer_create, name='offer_create'),
    path('online/', views.online_view, name='online_view'),
    path('nearby/', views.nearby_view, name='nearby_view'),
    path('bulk/', views.bulk_view, name='bulk_view'),
    path('food/', views.food_view, name='food_view'),
    path('(?P<slug>[\w-]+)/', views.offer_detail_view, name="offer_detail_view"),
]
