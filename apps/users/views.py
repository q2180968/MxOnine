from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm
from .models import UserProfile
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


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
        return render(request, 'login.html', {})

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
                    return render(request, 'login.html', {'msg': '用户未激活!'})
            else:
                return render(request, 'login.html', {'msg': '用户名密码错误!', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        reg_form = RegisterForm()
        return render(request, 'register.html', {'reg_form': reg_form})

    def post(self, request):
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.data['email']
            if UserProfile.objects.filter(username=username):
                return render(request, 'login.html', {'msg': '此用户已存在'})
            password = reg_form.data['password']
            user = UserProfile()
            user.username = username
            user.password = make_password(password)
            user.email = username
            user.is_active = False
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'reg_form': reg_form})
