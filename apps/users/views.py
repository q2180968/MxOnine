from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm
from .models import UserProfile, EmailVerifyRecord
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from utils.email_send import send_email
from datetime import datetime


# 自定义用户验证类
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户登录
class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.data['username']
            password = login_form.data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'users/login.html', {'msg': '用户未激活!'})
            else:
                return render(request, 'users/login.html', {'msg': '用户名密码错误!', 'login_form': login_form})
        else:
            return render(request, 'users/login.html', {'login_form': login_form})


# 用户注册
class RegisterView(View):
    def get(self, request):
        reg_form = RegisterForm()
        return render(request, 'users/register.html', {'reg_form': reg_form})

    def post(self, request):
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.data['email']
            if UserProfile.objects.filter(Q(username=username) | Q(email=username)):
                return render(request, 'users/login.html', {'msg': '此用户或邮箱已存在'})
            password = reg_form.data['password']
            user = UserProfile()
            user.username = username
            user.password = make_password(password)
            user.email = username
            user.is_active = False
            user.save()

            send_email(email=username, send_type='register')
            return render(request, 'users/login.html')
        else:
            return render(request, 'users/register.html', {'reg_form': reg_form})


# 用户激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code, send_type='register')
        if all_record:
            for record in all_record:
                if record.is_used == 0 and datetime.now() < record.expired_time:
                    record.is_used = True
                    record.save()
                    user = UserProfile.objects.get(email=record.email)
                    user.is_active = True
                    user.save()
                else:
                    error_msg = '验证码已失效！！！'
                    return render(request, 'users/code_expired.html', {'error_msg': error_msg})
        else:
            error_msg = '链接不存在'
            return render(request, 'users/code_expired.html', {'error_msg': error_msg})


# 忘记密码页面
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'users/forgetpwd.html', {'forget_form': forget_form})

    def post(self, requset):
        forget_form = ForgetPwdForm(requset.POST)
        if forget_form.is_valid():
            email = forget_form.data['email']
            status = send_email(email, 'forget')
            user = UserProfile.objects.filter(email=email)
            if user:
                if status == 1:
                    return render(requset, 'users/send_success.html')
                else:
                    return render(requset, 'users/forgetpwd.html', {'msg': '邮件发送失败！状态码{0}'.format(status)})
            else:
                return render(requset, 'users/forgetpwd.html', {'msg': '邮箱不存在！！'})
        else:
            return render(requset, 'users/forgetpwd.html', {'forget_form': forget_form})


# 密码重置
class ResetView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                if record.is_used == 0 and datetime.now() < record.expired_time:
                    reset_form = ResetPwdForm()
                    reset_form.data['active_code'] = active_code
                    return render(request, 'users/password_reset.html', {'reset_form': reset_form})
                else:
                    error_msg = '验证码已失效'
                    return render(request, 'users/code_expired.html', {'error_msg': error_msg})
        else:
            error_msg = '链接不存在'
            return render(request, 'users/code_expired.html', {'error_msg': error_msg})


# 修改密码
class ModifyPwdView(View):
    def post(self, request):
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            password1 = reset_form.data['password1']
            password2 = reset_form.data['password2']
            active_code = reset_form.data['active_code']
            all_record = EmailVerifyRecord.objects.filter(code=active_code)
            if all_record:
                for record in all_record:
                    if record.is_used == 0 and datetime.now() < record.expired_time:
                        record.is_used = 1
                        record.save()
                        email = record.email
                        user = UserProfile.objects.get(email=email)
                        user.password = make_password(password1)
                        user.save()
                        return render(request, 'users/login.html')
                    else:
                        error_msg = '验证码已失效'
                        return render(request, 'users/code_expired.html', {'error_msg': error_msg})
            else:
                error_msg = '链接不存在'
                return render(request, 'users/code_expired.html', {'error_msg': error_msg})
        else:
            return render(request, 'users/password_reset.html', {'reset_form': reset_form})
