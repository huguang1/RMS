"""
@author: 技术-小明
@time: 2019-04-03 17:19:52
@file: forms.py
@desc:
"""

from django import forms
from django.core.cache import cache

from utils.forms import FormMixin

from .models import User


class LoginForms(forms.Form, FormMixin):
    """
    登录表单验证
    'password': password,
    'username': username,
    'captcha': captcha,
    'captcha_id': self.imageCodeId
    """
    username = forms.CharField(max_length=64, required=True, error_messages={'required': "请输入用户名"})
    password = forms.CharField(max_length=128, required=True, error_messages={'required': "请输入密码"})
    captcha = forms.CharField(max_length=4, min_length=4, required=True, error_messages={'required': "请输入验证码"})
    captcha_id = forms.CharField(max_length=64, required=True)

    def clean(self):
        cleaned_data = super(LoginForms, self).clean()

        captcha_id = cleaned_data.get('captcha_id')
        captcha = cleaned_data.get('captcha')

        src_captcha = cache.get(captcha_id)
        if not src_captcha:
            raise forms.ValidationError('验证码有效期5分钟，您的验证码已经过期')

        if captcha.lower() != src_captcha.lower():
            raise forms.ValidationError('验证码错误')

        return cleaned_data


class CreateUserForms(forms.Form, FormMixin):
    """
    新建用户表单验证
    'username': username,
    'password1': password1,
    'password2': password2,
    'activation': activation,
    'user_desc': user_desc
    """
    username = forms.CharField(max_length=64, required=True, error_messages={'required': "请输入用户名"})
    password1 = forms.CharField(max_length=128, required=True, error_messages={'required': "请输入密码"})
    password2 = forms.CharField(max_length=128, required=True, error_messages={'required': "请输入密码"})
    activation = forms.IntegerField(max_value=1, min_value=0, required=True)
    user_desc = forms.CharField(max_length=255, required=False)

    # roles = forms.CheckboxInput()

    def clean(self):
        cleaned_data = super(CreateUserForms, self).clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError('两次密码不一致')

        username = cleaned_data.get('username')
        try:
            user = User.objects.get(username=username)

        except:
            return cleaned_data
        else:
            raise forms.ValidationError('用户 %s 已经被注册！' % user.username)
