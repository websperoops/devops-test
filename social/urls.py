from .views import *
from django.conf.urls import url


urlpatterns = [
    url(r'^/mentions',mentions),
    url(r'^/messages', messages),
    url(r'/reply_to_tweet', reply),
    url(r'/new_tweet', updateStatus),


    url(r'^', index)
]
