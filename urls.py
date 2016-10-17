# coding: utf-8

from django.conf.urls import url

from beatle import views


urlpatterns = [
    url(r'', views.endpoint)
]
