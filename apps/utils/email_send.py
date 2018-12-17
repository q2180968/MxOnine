from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from MxOnline import settings


def random_str(rangelength=16):
    str = ''
    char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = len(char) - 1
    random = Random()
    for i in range(rangelength):
        str += char[random.randint(0, length)]
    return str


def send_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = '幕学在线网注激活链接'
        email_body = '请点击下面链接激活您的账号：\n http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        return send_status
    elif send_type == 'forget':
        email_title = '幕学在线网密码重置链接'
        email_body = '请点击下面链接重置您的账号密码：\n http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        return send_status
    elif send_type == 'update_email':
        email_title = '幕学在线网邮箱修改验证码'
        email_body = '您的邮箱验证码为{0}'.format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        return send_status
