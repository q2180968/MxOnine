from django.db import models
from datetime import datetime
from organization.models import *


# Create your models here.
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name='机构', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='课程名称')
    desc = models.CharField(max_length=300, verbose_name='简介')
    detail = models.TextField(verbose_name='课程详情')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播图')
    teacher = models.ForeignKey(Teacher, verbose_name='教师', on_delete=models.CASCADE)
    degree = models.CharField(verbose_name='难度', choices=(('easy', '初级'), ('normal', '普通'), ('hard', '困难')),
                              max_length=10, default='easy')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长（分钟）')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='点赞数')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图', max_length=100,
                              default='course/default.png')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(max_length=50, verbose_name='类别', default='')
    tag = models.CharField(max_length=50, verbose_name='标签', default='')
    youneed_know = models.CharField(verbose_name='课程须知', max_length=300, default='')
    teacher_tell = models.CharField(verbose_name='老师告诉你', max_length=300, default='')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta():
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='章节名称')
    learn_time = models.IntegerField(default=0, verbose_name='学习时间')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta():
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='', verbose_name='名称')
    learn_time = models.IntegerField(default=0, verbose_name='学时时长')
    url = models.CharField(max_length=200, verbose_name='访问地址', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta():
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='', verbose_name='名称')
    download = models.FileField(upload_to='video/%Y/%m', verbose_name='资源文件', max_length=200)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta():
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
