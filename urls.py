from django.conf.urls import patterns, url

from hermes import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^boards/(?P<board_id>\d+)/$', views.board, name='board'),
    url(r'^boards/(?P<board_id>\d+)/delete/(?P<post_id>\d+)/$', views.delete, name='delete'),
    url(r'^boards/(?P<board_id>\d+)/ban/(?P<post_id>\d+)/$', views.ban, name='ban'),
    url(r'^boards/(?P<board_id>\d+)/new/$', views.post, name='new'),
    url(r'^boards/(?P<board_id>\d+)/thread/(?P<thread_id>\d+)/$', views.thread, name='thread'),
    url(r'^boards/(?P<board_id>\d+)/thread/(?P<thread_id>\d+)/reply/$', views.reply, name='reply'),
    url(r'^(?P<static_html>.+)/$', views.static, name='static'),
)
