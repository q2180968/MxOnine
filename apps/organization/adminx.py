import xadmin
from .models import *


class CityDictAdmin(object):
    pass


xadmin.site.register(CityDict, CityDictAdmin)


class CourseOrgAdmin(object):
    list_display = ['name', 'address']
    # list_filter = ['email', 'send_type', 'send_time']
    # search_fields = ['email']


xadmin.site.register(CourseOrg, CourseOrgAdmin)


class TeacherAdmin(object):
    pass


xadmin.site.register(Teacher, TeacherAdmin)
