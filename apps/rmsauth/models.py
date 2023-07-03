from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser


# 用户管理
class UserManager(BaseUserManager):
    def _create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError('请传入用户名！')
        if not password:
            raise ValueError('请传入密码！')

        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, **kwargs):
        kwargs['is_superuser'] = False
        kwargs['is_staff'] = True
        return self._create_user(username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_ordinaryadmin'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, **kwargs)


# 管理员用户
class User(AbstractBaseUser, PermissionsMixin):
    """
    username: 帐号
    is_active: 是否冻结
    roles： 关联角色，权限控制
    remark: 备注
    is_superuser： 超级管理类型
    is_ordinaryadmin: 普通管理员
    last_login:上次登录时间
    last_login_ip:上次登录IP
    roles: 角色
    group: 招聘组
    now_ip:当前登录IP
    u_time:更新时间
    data_joined：创建时间
    """
    username = models.CharField(max_length=64, unique=True, null=False)
    is_superuser = models.BooleanField(null=False, default=False)
    is_ordinaryadmin = models.BooleanField(null=False, default=False)
    is_active = models.BooleanField(null=False, default=True)
    is_staff = models.BooleanField(null=False, default=False)
    user_desc = models.CharField(max_length=255, null=True)
    last_login_ip = models.CharField(max_length=32, null=False, default='127.0.0.1')
    now_ip = models.CharField(max_length=32, null=False, default='127.0.0.1')
    roles = models.ManyToManyField(to="Role")
    group = models.ForeignKey(to="Group", null=True, blank=True, on_delete=models.CASCADE, related_name="users")
    u_time = models.DateTimeField(auto_now=True)
    data_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'rms_user'
        ordering = ['id']


class Group(models.Model):
    """
    招聘组
    title: 分组名称
    """

    title = models.CharField(max_length=64, null=False, verbose_name="招聘分组")

    class Meta:
        db_table = 'rms_group'
        ordering = ['id']


class Menu(models.Model):
    """
    菜单表
    一级菜单
    title: 菜单标题
    """
    title = models.CharField(max_length=32)

    class Meta:
        db_table = 'rms_menu'
        ordering = ['id']


class Permission(models.Model):
    """
    权限表
    title: 权限标题
    url：包含正则的url，即这个权限能访问的url
    parent: 自关联， 等于NULL时 是二级菜单 (显示在菜单栏中)，不为空时，为二级菜单对应页面的权限 (不显示在权限菜单栏中)
    menu: 菜单 (一组权限)
    method: 请求方式 GET， PUT， POST， DELETE
    """
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=128)
    method = models.CharField(max_length=16)
    parent = models.ForeignKey(to="Permission", null=True, blank=True, on_delete=models.CASCADE)
    menu = models.ForeignKey(to="Menu", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'rms_permission'
        ordering = ['id']


class Role(models.Model):
    """
    角色表
    name: 角色名称
    permissions: 角色关联的权限
    """
    name = models.CharField(max_length=32, null=False, unique=True)
    permissions = models.ManyToManyField(to="Permission", blank=True)

    class Meta:
        db_table = 'rms_role'
        ordering = ['id']


class White(models.Model):
    """
    白名单
    url: 白名单可以访问的 url
    """
    url = models.CharField(max_length=128)
    method = models.CharField(max_length=16, default='GET')

    class Meta:
        db_table = 'rms_white_list'
        ordering = ['id']
