
from django.conf.urls import url

from openwx import views

# app_name = 'lists'
urlpatterns = [
    url(r'^$', views.access_token, name='access_token'),
]