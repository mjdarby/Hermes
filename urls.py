from django.conf.urls import patterns, url

from hermes import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<board_name>[a-zA-Z0-9]+)/$', views.board, name='board'),
    url(r'^(?P<board_name>[a-zA-Z0-9]+)/delete/(?P<post_id>\d+)/$', views.delete, name='delete'),
    url(r'^(?P<board_name>[a-zA-Z0-9]+)/ban/(?P<post_id>\d+)/$', views.ban, name='ban'),
    url(r'^(?P<board_name>[a-zA-Z0-9]+)/new/$', views.post, name='new'),
    url(r'^(?P<board_name>[a-zA-Z0-9]+)/(?P<thread_id>\d+)/$', views.thread, name='thread'),
    url(r'^(?P<board_name>[a-zA-Z0-9]+)/(?P<thread_id>\d+)/autosage/$', views.autosage, name='autosage'),
    url(r'^(?P<board_name>[a-zA-Z0-9]+)/(?P<thread_id>\d+)/sticky/$', views.sticky, name='sticky'),
    url(r'^(?P<board_name>[a-zA-Z0-9]+)/(?P<thread_id>\d+)/unsticky/$', views.unsticky, name='unsticky'),
    url(r'^(?P<board_name>[a-zA-Z0-9]+)/(?P<thread_id>\d+)/reply/$', views.reply, name='reply'),
    url(r'^static/(?P<static_html>.+)/$', views.static, name='static'),
)
