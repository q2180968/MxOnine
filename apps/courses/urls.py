from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'course_list/$', CourseListView.as_view(), name='course_list'),
    url(r'course_detail/(?P<course_id>\d+)', CourseDetailView.as_view(), name='course_detail'),
]
