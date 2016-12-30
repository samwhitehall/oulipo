from django.conf.urls import url

from poem.views import create, view

urlpatterns = [
    url(r'poem/$', create),
    url(r'poem/(?P<slug>[-\w]+)/$', view),
]
