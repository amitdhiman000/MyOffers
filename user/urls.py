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
    url(r'^$', views.home_view, name='home_view'),
    url(r'^signin/$', views.signin_view, name='signin_view'),
    url(r'^signin-auth/$', views.signin_auth, name='signin_auth'),
    url(r'^signup/$', views.signup_view, name='signup_view'),
    url(r'^signup-auth/$', views.signup_auth, name='signup_auth'),
    url(r'^signup-success/$', views.signup_success_view, name='signup_success_view'),
    url(r'^signout/$', views.signout, name='signout'),
    # user profile tabs
    url(r'^account/$', views.user_account_view, name='user_account_view'),
    url(r'^messages/$', views.user_messages_view, name='user_messages_view'),
    url(r'^stats/$', views.user_stats_view, name='user_stats_view'),
    url(r'^wishlist/$', views.user_wishlist_view, name='user_wishlist_view'),
    url(r'^settings/$', views.user_settings_view, name='user_settings_view'),
    url(r'^update/$', views.user_update, name='user_update'),
    url(r'^topic-selected/$', views.user_topic_selected, name='user_topic_selected'),
]
