from .models import *
import xadmin
import xadmin.views


# 设置主题信息
class BaseSetting(object):
    enable_themes = True
    # use_bootswatch = True


xadmin.site.register(xadmin.views.BaseAdminView, BaseSetting)


# 设置LOGO，尾部信息
class GloabSetting(object):
    site_title = '幕学在线'
    site_footer = '@幕学在线'
    # 将菜单设置为可折叠
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

xadmin.site.unregister(UserProfile)


class UserProfileAdmin(object):
    pass


xadmin.site.register(UserProfile, UserProfileAdmin)
