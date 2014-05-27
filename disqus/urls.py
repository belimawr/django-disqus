#coding: utf-8
from django.conf.urls import patterns, url
from django.shortcuts import redirect

from . import views

urlpatterns = patterns('',
    url(r'^ajax_sso/$', views.ajax_sso, name='ajax_sso'),
    url(r'^ajax_show_comments/$', views.ajax_show_comments, name='ajax_show_comments'),
)
