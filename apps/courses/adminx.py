import xadmin
from .models import *


class CourseAdmin(object):
    pass


xadmin.site.register(Course, CourseAdmin)


class LessonAdmin(object):
    pass


xadmin.site.register(Lesson, LessonAdmin)


class VideoAdmin(object):
    pass


xadmin.site.register(Video, VideoAdmin)


class CourseResourceAdmin(object):
    pass


xadmin.site.register(CourseResource, CourseResourceAdmin)
