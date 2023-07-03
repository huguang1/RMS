"""
@author: 技术-小明
@time: 2019-04-21 16:38:34
@file: serializers.py
@desc:
"""

from rest_framework import serializers

from .models import Menu
from .models import Permission
from .models import Role
from .models import User
from .models import Group


class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title")


class MenuSerializers(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ("id", "title")


class SubPermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id", "title")


class PermissionSerializers(serializers.ModelSerializer):
    """
    title: 权限标题
    url：包含正则的url，即这个权限能访问的url
    parent: 自关联， 等于NULL时 是二级菜单 (显示在菜单栏中)，不为空时，为二级菜单对应页面的权限 (不显示在权限菜单栏中)
    menu: 菜单 (一组权限)
    method: 请求方式 GET， PUT， POST， DELETE
    """
    menu = MenuSerializers()
    parent = SubPermissionSerializers()

    class Meta:
        model = Permission
        fields = ("id", "title", "url", "parent", "menu", "method")


class RolePermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id"]


class RoleSerializers(serializers.ModelSerializer):
    permissions = RolePermissionSerializers(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ("id", "name", "permissions")


class RoleUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")


class UserSerializers(serializers.ModelSerializer):
    roles = RoleUserSerializers(many=True, read_only=True)
    group = GroupSerializers()

    class Meta:
        model = User
        fields = ("id", "username", "is_active", "user_desc", "last_login", "last_login_ip", "roles", "group")
