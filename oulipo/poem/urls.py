from django.conf.urls import url

from poem.views import create, poem_view

urlpatterns = [
    url(r'poem/$', create, name='new_poem'),
    url(r'poem/(?P<slug>[-\w]+)/$', poem_view, name='existing_poem'),
]
