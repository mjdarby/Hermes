from django.conf.urls import patterns, url

from hermes import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'))
