import xadmin
from .models import *


class CityDictAdmin(object):
    pass


xadmin.site.register(CityDict, CityDictAdmin)


class CourseOrgAdmin(object):
    pass


xadmin.site.register(CourseOrg, CourseOrgAdmin)


class TeacherAdmin(object):
    pass


xadmin.site.register(Teacher, TeacherAdmin)
