from django.db import models


# Create your models here.
class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=200, verbose_name='描述')
    add_time = models.DateTimeField(default='', verbose_name='添加时间')

    class Meta():
        verbose_name = '城市信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=20, default='', verbose_name='机构名称')
    desc = models.TextField(default='', verbose_name='机构描述')
    tag = models.CharField(max_length=50, default='', verbose_name='标签')
    category = models.CharField(max_length=20, default='gr', verbose_name='机构类别',
                                choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')))
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(default='org/default.png', upload_to='org/%Y/%m', verbose_name='封面图')
    address = models.ForeignKey(CityDict, verbose_name='所在城市', on_delete=models.CASCADE)
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')
    add_time = models.DateTimeField(default='', verbose_name='添加时间')

    class Meta():
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name='归属机构', on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='', verbose_name='教师姓名')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_company = models.CharField(max_length=50, verbose_name='工作单位', default='')
    work_position = models.CharField(max_length=50, verbose_name='工作职位', default='')
    points = models.CharField(max_length=200, verbose_name='特色', default='')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    age = models.IntegerField(default=0, verbose_name='年龄')
    image = models.ImageField(upload_to='', default='', verbose_name='头像')
    add_time = models.DateTimeField(default='', verbose_name='添加时间')

    class Meta():
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
