from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.

# 用户信息表
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='昵称', default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(max_length=6, verbose_name='性别', choices=(('male', '男'), ('famale', '女')), default='male')
    address = models.CharField(max_length=200, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机号码', null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', verbose_name='头像', max_length=200)

    class Meta():
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 邮箱验证记录表
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.CharField(max_length=200, verbose_name='邮箱地址')
    send_type = models.CharField(max_length=100, verbose_name='验证码类型',
                                 choices=(('register', '用户注册'), ('forget', '忘记密码'), ('update_email', '修改邮箱')))
    send_time = models.DateTimeField(verbose_name='发送时间', default=datetime.now)

    def __str__(self):
        return self.email

    class Meta():
        verbose_name = '邮箱验证'
        verbose_name_plural = verbose_name


# 轮播图
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='static/banner/%Y/%m', verbose_name='轮播图片', max_length=200)
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    class Meta():
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
