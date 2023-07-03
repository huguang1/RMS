"""
@author: 技术-小明
@time: 2019-04-05 18:59:42
@file: middleware.py
@desc: 权限控制中间件
"""

import re

from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect

from . import common


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 当前url
        current_url = request.path_info
        # 请求方式
        current_method = request.method
        # 当前用户
        current_user = request.user


        # 白名单
        white_obj = common.get_whith()
        for whith in white_obj:
            if re.match(whith['url'], current_url) and whith['method'] == current_method:
                return None

        # 判定是否登录
        if not current_user.is_authenticated:
            redirect_url = "/account/login/?next=%s" % current_url
            return redirect(redirect_url)

        # 超级管理员
        if request.user.is_superuser:
            return None

        # 没有权限页面 和 首页
        if current_url == '/' and current_method == "GET":
            return None

        # 获取当前用户所有权限
        flag = False
        permissions = request.session.get("rms_permission_url_list_key")
        for permission in permissions:
            reg = "^%s$" % permission.get('url')
            if re.match(reg, current_url) and permission.get('method') == current_method:
                flag = True
        if flag:
            return None
        else:
            return redirect(reverse("account:notpermission"))
