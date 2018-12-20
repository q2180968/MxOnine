from django import forms
from operation.models import UserAsk
import re


class UserAskForm(forms.ModelForm):
    class Meta():
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    # 自定义验证写法固定，clean开头_后跟上字段名称
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1(3|4|5|7|8)\d{9}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号非法！！！', code='mobile_invalid')
