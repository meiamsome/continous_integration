from django.conf.urls import patterns, include, url
import api_views

urlpatterns = patterns('',
    url(r'^(?P<repository_name>[^/]*/[^/]*)/', include(patterns('',
        url(r'^hook/$', api_views.hook_url)
    )))
)