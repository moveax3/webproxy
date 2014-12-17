from django.conf.urls import patterns, include, url
from views import index, page, image, script, style

urlpatterns = patterns('',
    url(r'^$', 'webproxy.views.index', name='index'),
    url(r'^viewpage/.*$', 'webproxy.views.page', name='page'),
    url(r'^viewimage/.*$', 'webproxy.views.image', name='image'),
    url(r'^viewscript/.*$', 'webproxy.views.script', name='script'),
    url(r'^viewstyle/.*$', 'webproxy.views.style', name='style'),
)
