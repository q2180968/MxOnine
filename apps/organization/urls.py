from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'list/$', OrganizationView.as_view(), name='org_list')
]
