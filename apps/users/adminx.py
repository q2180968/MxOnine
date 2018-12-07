from .models import *
import xadmin
import xadmin.views


class BaseSetting(object):
    enable_themes = True
    # use_bootswatch = True


xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)


class GloabSetting(object):
    site_title = '幕学在线'
    site_footer = '@幕学在线'
    menu_style = 'accordion'


xadmin.site.register(xadmin.views.CommAdminView, GloabSetting)


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    list_filter = ['email', 'send_type', 'send_time']
    search_fields = ['email']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class BannerAdmin(object):
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图片', max_length=200)
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='创建时间')

    list_display = ['title', 'add_time']
    list_filter = ['title', 'add_time', 'index']
    search_fields = ['title']


xadmin.site.register(Banner, BannerAdmin)
