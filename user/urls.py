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
    path('signin/', views.signin_view, name='signin_view'),
    path('signin-auth/', views.signin_auth, name='signin_auth'),
    path('signup/', views.signup_view, name='signup_view'),
    path('signup-auth/', views.signup_auth, name='signup_auth'),
    path('signup-success/', views.signup_success_view, name='signup_success_view'),
    path('signout/', views.signout, name='signout'),
    # user profile tabs
    path('account/', views.user_account_view, name='user_account_view'),
    path('messages/', views.user_messages_view, name='user_messages_view'),
    path('stats/', views.user_stats_view, name='user_stats_view'),
    path('wishlist/', views.user_wishlist_view, name='user_wishlist_view'),
    path('settings/', views.user_settings_view, name='user_settings_view'),
    path('update/', views.user_update, name='user_update'),
    path('updatepass/', views.user_update_password, name='user_update_password'),
    path('topic-selected/', views.user_topic_selected, name='user_topic_selected'),
]
