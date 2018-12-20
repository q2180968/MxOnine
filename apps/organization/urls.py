from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'list/$', OrganizationView.as_view(), name='org_list'),
    url(r'add_ask/$', UserAskView.as_view(), name='add_ask'),
    url(r'detail/(?P<org_id>\d+)/$', OrgDetailHomeView.as_view(), name='detail'),
    url(r'course/(?P<org_id>\d+)/$', OrgDetailCourseView.as_view(), name='org_course'),
    url(r'desc/(?P<org_id>\d+)/$', OrgDetailDescView.as_view(), name='org_desc'),
    url(r'teacher/(?P<org_id>\d+)/$', OrgDetailTeacherView.as_view(), name='org_teacher'),

    url(r'add_fav/$', AddFavView.as_view(), name='add_fav')
]
