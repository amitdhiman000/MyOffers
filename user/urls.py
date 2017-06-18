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
	url(r'^signin/$', views.signin_view, name='signin_view'),
	url(r'^signin-auth/$', views.signin_auth, name='signin_auth'),
	url(r'^signup/$', views.signup_view, name='signup_view'),
	url(r'^signup-register/$', views.signup_register, name='signup_register'),
	url(r'^signup-success/$', views.signup_success_view, name='signup_success_view'),
	url(r'^signout/$', views.signout, name='signout'),
    ## user profile tabs
	url(r'^profile/$', views.profile_view, name='profile_view'),
	url(r'^info/$', views.user_info_view, name='user_info_view'),
	url(r'^topics/$', views.user_topics_view, name='user_topics_view'),
	url(r'^topic-selected/$', views.user_topic_selected, name='user_topic_selected'),
	url(r'^mails/$', views.user_mails_view, name='user_mails_view'),
	url(r'^stats/$', views.user_stats_view, name='user_stats_view'),
	url(r'^settings/$', views.user_settings_view, name='user_settings_view'),
]
