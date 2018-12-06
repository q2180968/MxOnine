from django.db import models
from datetime import datetime
from courses.models import *
from users.models import *


# Create your models here.
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    mobile = models.CharField(max_length=11, verbose_name='手机号码 ')
    course_name = models.CharField(max_length=50, verbose_name='咨询课程名')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta():
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    comments = models.CharField(max_length=100, verbose_name='评论', default='')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta():
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.name


class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    fav_id = models.IntegerField(verbose_name='数据id', default=0)
    fav_type = models.IntegerField(default=1, choices=((1, '讲师'), (2, '机构'), (3, '课程')))
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta():
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name='接受用户')
    message = models.CharField(max_length=500, verbose_name='消息内容')
    has_read = models.BooleanField(default=0, verbose_name='是否已读')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta():
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)

    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta():
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.name
