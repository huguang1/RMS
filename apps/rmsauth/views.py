import logging
# from treelib import Node, Tree

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import QueryDict
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
# from django.db.models import Q

from utils import restful
from utils.captcha.captcha import captcha
from utils.pagination import get_pagination_data
from .forms import CreateUserForms
from .forms import LoginForms
from .models import Menu
from .models import Permission
from .models import Role
from .models import User
from .models import Group
from .serializers import MenuSerializers
from .serializers import PermissionSerializers
from .serializers import RoleSerializers
from .serializers import UserSerializers
from .serializers import GroupSerializers
from .init_permission import init_permission

logger = logging.getLogger(__name__)


class NotPermissionView(View):
    """
    没有权限页面
    """
    def get(self, request):
        return render(request, 'user/not_permission.html')


class LoginView(View):
    """
    用户登录
    """

    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        form = LoginForms(request.POST)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # 用户验证
        user = authenticate(request, username=username, password=password)
        if not user:
            return restful.params_error(message="用户名或者密码错误！")
            # 判断用户是否被冻结
        if not user.is_active:
            return restful.unauth(message="您的账号已经被冻结了！")

        login(request, user)
        init_permission(request)
        return restful.ok()


class LogoutView(View):
    """
    退出登录
    """

    def get(self, request):
        # 退出登录
        logout(request)
        request.session.flush()
        # 跳转到登录页面
        return redirect(reverse('rms_auth:login'))


class CaptchaView(View):
    """
    获取图片验证码
    """

    def get(self, request):
        # 上一个验证码id
        pre_code_id = request.GET.get("p")
        # 当前验证码id
        cur_code_id = request.GET.get("c")
        # 删除上一个验证码
        if pre_code_id:
            cache.delete(pre_code_id)
        # 生成验证码
        name, text, img = captcha.generate_captcha()
        # 存入缓存中, 验证码有效期5分钟
        cache.set(cur_code_id, text.lower(), 5 * 60)
        # 返回图片
        return HttpResponse(img, content_type='image/jpg')


class UserView(View):
    """
    用户管理
    """

    def get(self, request):
        try:
            roles = Role.objects.all()
            groups = Group.objects.all()
            users = User.objects.prefetch_related('roles', 'group').filter(is_superuser=False).exclude(
                id=request.user.id)
            paginator = Paginator(users, settings.PAGE_COUNT)
            obj_page = paginator.page(1)
            context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
            context = {'data': obj_page, 'count': len(users), 'roles': roles, 'groups': groups}
            context.update(context_data)
        except Exception as e:
            logger.error(e)
        return render(request, 'user/rms_user.html', context=context)

    # 添加用户
    def post(self, request):
        roles = request.POST.getlist('roles')
        form = CreateUserForms(request.POST)
        try:
            group_id = int(request.POST.get('group', 0))
        except:
            group_id = 0

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            activation = form.cleaned_data.get('activation')
            user_desc = form.cleaned_data.get('user_desc')
            # roles = form.cleaned_data.get('roles')

            kwargs = {'is_active': False if activation == 1 else True, 'user_desc': user_desc}
            if group_id:
                group = Group.objects.get(id=group_id)
                kwargs.update({'group': group})

            user = User.objects.create_user(username=username, password=password, **kwargs)

            if roles:
                roles_id_list = [int(role) for role in roles]
                roles_add = Role.objects.filter(id__in=roles_id_list)
                user.roles.add(*roles_add)
        else:
            return restful.params_error(message=form.get_errors())
        return restful.ok()

    # 编辑用户
    def put(self, request):
        data = QueryDict(request.body)
        try:
            group_id = int(data.get('group'))
        except:
            group_id = 0
        try:
            user_id = int(data.get('user_id'))
        except:
            user_id = 0
        roles = data.getlist('roles')
        activation = data.get('activation')
        user_desc = data.get('user_desc')
        user_id = data.get('user_id')

        if not user_id:
            return restful.params_error(message="用户不存在")

        try:
            user = User.objects.prefetch_related('roles').get(id=user_id)

            if group_id:
                group = Group.objects.get(id=group_id)
                user.group = group

            if roles:
                src_roles_id_list = []
                update_roles = [int(role) for role in roles]
                src_roles = user.roles.all()
                for role in src_roles:
                    if role.id not in update_roles:
                        user.roles.remove(role)
                    else:
                        src_roles_id_list.append(role.id)
                update_roles_id_list = list(set(update_roles).difference(set(src_roles_id_list)))
                if update_roles_id_list:
                    add_roles = Role.objects.filter(id__in=update_roles_id_list)
                    user.roles.add(*add_roles)

            user.is_active = (False if activation == '1' else True)
            user.user_desc = user_desc
            user.save()

            return restful.ok()

        except Exception as e:
            logger.error(e)
            return restful.server_error(message="用户不存在， 请刷新数据重试")

    # 删除用户
    def delete(self, request):
        data = QueryDict(request.body)
        try:
            user_id = int(data.get('user_id', 0))
        except:
            user_id = 0

        if not user_id:
            return restful.params_error(message="用户不存在， 请刷新数据重试")
        try:
            User.objects.get(id=user_id).delete()
            return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="用户不存在， 请刷新数据重试")


class UserListView(View):
    def get(self, request):
        try:
            page = int(request.GET.get('p', 1))
        except:
            page = 1
        # 一页显示多少条数据
        one_page_count = settings.PAGE_COUNT
        start = (page - 1) * one_page_count
        end = start + one_page_count

        users = User.objects.prefetch_related('roles').filter(is_superuser=False).exclude(id=request.user.id)
        # 总共有多少条数据
        count = len(users)
        # 一页数据
        data = users[start:end]
        # 序列化
        serializer = UserSerializers(data, many=True)
        # 序列化后的数据
        tmp_data = serializer.data

        return restful.result(data={"data": tmp_data, "count": count, "page_count": one_page_count})


# 修改密码
class ChangePasswordView(View):
    # 修改其他用户密码
    def post(self, request):
        user_id = request.POST.get("user_id", 0)
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not password1 or not password2 or password1 != password2:
            return restful.params_error(message="两次输入的密码不一致")

        # if password1 != password2:
        #     return restful.params_error(message="两次输入的密码不一致")

        if not user_id:
            return restful.params_error(message="用户不存在")

        user_id = int(user_id)
        try:
            user = User.objects.get(id=user_id)
            user.set_password(password1)
            user.save()
            return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="密码修改失败， 请刷新数据重试")

    # 修改当前用户密码
    def put(self, request):
        data = QueryDict(request.body)
        password1 = data.get("password1")
        password2 = data.get("password2")

        if not password1 or not password2 or password1 != password2:
            return restful.params_error(message="两次输入的密码不一致")

        # if password1 != password2:
        #     return restful.params_error(message="两次输入的密码不一致")

        try:
            user = request.user
            user.set_password(password1)
            user.save()
            return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="密码修改失败， 请刷新数据重试")


class GroupView(View):
    def get(self, request):
        try:
            groups = Group.objects.all()
            paginator = Paginator(groups, settings.PAGE_COUNT)
            obj_page = paginator.page(1)
            context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
            context = {'data': obj_page, 'count': len(groups)}
            context.update(context_data)

            return render(request, 'user/user_group.html', context=context)
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="页面加载失败， 请刷新数据重试")

    def post(self, request):
        groupname = request.POST.get("groupname")
        if not groupname:
            return restful.params_error(message="请输入用户组名")

        try:
            Group.objects.create(title=groupname)
            return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.params_error(message="请输入用户组名")

    def put(self, request):
        data = QueryDict(request.body)
        group_title = data.get("title")
        try:
            group_id = int(data.get("group_id", 0))
        except:
            group_id = 0

        if not group_title or not group_id:
            return restful.params_error(message="请输入用户组名")

        try:
            group = Group.objects.get(id=group_id)
            group.title = group_title
            group.save()
            return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.params_error(message="请输入用户组名")

    def delete(self, request):
        data = QueryDict(request.body)
        try:
            group_id = int(data.get("group_id", 0))
        except:
            group_id = 0

        if not group_id:
            return restful.params_error(message="用户组不存在")

        try:
            Group.objects.get(id=group_id).delete()
            return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.params_error(message="用户组不存在")


class GroupListView(View):
    def get(self, request):
        try:
            page = int(request.GET.get('p', 1))
        except:
            page = 1
        # 一页显示多少条数据
        one_page_count = settings.PAGE_COUNT
        start = (page - 1) * one_page_count
        end = start + one_page_count

        groups = Group.objects.all()
        # 总共有多少条数据
        count = len(groups)
        # 一页数据
        data = groups[start:end]
        # 序列化
        serializer = GroupSerializers(data, many=True)
        # 序列化后的数据
        tmp_data = serializer.data

        return restful.result(data={"data": tmp_data, "count": count, "page_count": one_page_count})


class MenuView(View):
    """
    一级菜单管理
    """

    def get(self, request):
        try:
            menus = Menu.objects.all()
            paginator = Paginator(menus, settings.PAGE_COUNT)
            obj_page = paginator.page(1)
            context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
            context = {'data': obj_page, 'count': len(menus)}
            context.update(context_data)

            return render(request, 'user/rms_user_menu.html', context=context)
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="页面加载失败， 请刷新数据重试")

    def post(self, request):
        name = request.POST.get("name")
        if not name:
            return restful.params_error(message="请输入菜单名称")
        else:
            try:
                menu = Menu(title=name)
                menu.save()
                return restful.ok()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="添加菜单失败， 请刷新数据重试")

    def delete(self, request):
        data = QueryDict(request.body)
        try:
            id = int(data.get('id', 0))
        except:
            id = 0

        if not id:
            return restful.params_error(message="菜单不存在")
        else:
            try:
                Menu.objects.get(id=id).delete()
                return restful.ok()
            except Exception as e:
                logger.error(e)
                return restful.server_error(message="菜单不存在")

    def put(self, request):
        data = QueryDict(request.body)

        title = data.get('title')

        try:
            id = int(data.get('id', 0))
        except:
            id = 0

        if id and title:
            try:
                menu = Menu.objects.get(id=id)
                menu.title = title
                menu.save()
                return restful.ok()
            except Exception as e:
                logger.error(e)
                return restful.params_error(message="修改菜单失败， 请刷新数据重试")


class MenuListView(View):
    def get(self, request):
        try:
            page = int(request.GET.get('p', 1))
        except:
            page = 1
        # 一页显示多少条数据
        one_page_count = settings.PAGE_COUNT
        start = (page - 1) * one_page_count
        end = start + one_page_count

        menus = Menu.objects.all()
        # 总共有多少条数据
        count = len(menus)
        # 一页数据
        data = menus[start:end]
        # 序列化
        serializer = MenuSerializers(data, many=True)
        # 序列化后的数据
        tmp_data = serializer.data

        return restful.result(data={"data": tmp_data, "count": count, "page_count": one_page_count})


class PermissionView(View):
    """
    权限管理
    """

    def get(self, request):

        try:
            menus = Menu.objects.all()
            permissions = Permission.objects.select_related('menu').all()

            tmp_list = []
            for menu in menus:
                tmp_list.append({"id": str(menu.id), "title": menu.title + " (菜单)", "data_type": '1'})

            for permission in permissions:
                if not permission.parent:
                    tmp_list.append({"id": str(permission.id), "title": permission.title, "data_type": '0'})

            paginator = Paginator(permissions, settings.PAGE_COUNT)
            obj_page = paginator.page(1)
            context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
            context = {'data': obj_page, 'count': len(permissions), 'data_tan': tmp_list}
            context.update(context_data)

        except Exception as e:
            logger.error(e)
            return restful.server_error(message="404")
        else:
            return render(request, 'user/rms_user_permission.html', context=context)

    def post(self, request):
        """
        'title': title,
        'url': url,
        'p_type': parentType,
        'p_id': parentValue
        :param request:
        :return:
        """

        title = request.POST.get("title")
        url = request.POST.get("url")
        method = request.POST.get("method")
        p_type = request.POST.get("p_type")
        try:
            p_id = int(request.POST.get("p_id", 0))
        except:
            p_id = 0

        if title and url and p_type and p_id and method:
            try:
                if p_type == '0':
                    permission = Permission.objects.get(id=p_id)
                    Permission.objects.create(title=title, url=url, parent=permission, method=method)
                elif p_type == '1':
                    menu = Menu.objects.get(id=p_id)
                    Permission.objects.create(title=title, url=url, menu=menu, method=method)

                return restful.ok()
            except Exception as e:
                logger.error(e)
                return restful.params_error(message="请输入正确的参数")

        else:
            return restful.params_error(message="请输入正确的参数")

    def delete(self, request):
        data = QueryDict(request.body)

        try:
            cur_id = int(data.get("cur_id"))
            permission = Permission.objects.get(id=cur_id)
            permission.delete()
        except Exception as e:
            logger.error(e)
            return restful.params_error(message="删除权限失败，请刷新数据重试")
        else:
            return restful.ok()

    def put(self, request):
        data = QueryDict(request.body)

        title = data.get("title")
        url = data.get("url")
        method = data.get("method")
        p_type = data.get("p_type")
        try:
            p_id = int(data.get("p_id", 0))
            cur_id = int(data.get("cur_id", 0))
        except:
            p_id = 0
            cur_id = 0

        if title and url and p_type and p_id and method and cur_id:
            try:
                permission = Permission.objects.get(id=cur_id)

                if p_type == '0':
                    parent_permission = Permission.objects.get(id=p_id)
                    permission.parent = parent_permission
                    permission.title = title
                    permission.url = url
                    permission.method = method
                    permission.menu = None
                elif p_type == '1':
                    menu = Menu.objects.get(id=p_id)
                    permission.menu = menu
                    permission.title = title
                    permission.url = url
                    permission.method = method
                    permission.parent = None

                permission.save()
            except Exception as e:
                logger.error(e)
                return restful.params_error(message="请输入正确的参数")
            else:
                return restful.ok()
        else:
            return restful.params_error(message="请输入正确的参数")


class PermissionListView(View):
    def get(self, request):
        try:
            page = int(request.GET.get('p', 1))
        except:
            page = 1

        # 一页显示多少条数据
        one_page_count = settings.PAGE_COUNT
        start = (page - 1) * one_page_count
        end = start + one_page_count

        permissions = Permission.objects.select_related('menu').all()

        # 总共有多少条数据
        count = len(permissions)
        # 一页数据
        data = permissions[start:end]
        # 序列化
        serializer = PermissionSerializers(data, many=True)
        # 序列化后的数据
        tmp_data = serializer.data

        return restful.result(data={"data": tmp_data, "count": count, "page_count": one_page_count})


class RoleView(View):
    """
    角色管理
    """

    def get(self, request):

        try:
            permissions = Permission.objects.select_related('menu').all()

            # 一级
            data_one = dict()
            # 二、三级
            data_two = dict()

            for permission in permissions:
                if permission.menu:
                    data_one[permission.menu.id] = {'id': permission.menu.id, 'title': permission.menu.title}
                    data_two[permission.id] = {'id': permission.id, 'title': permission.title,
                                               'p_id': permission.menu.id}
                if permission.parent:
                    data_two[str(permission.id)] = {'id': permission.id, 'title': permission.title,
                                                    'p_id': permission.parent.menu.id}
            data_list = []
            for key, value in data_one.items():
                tmp_menu = dict()
                tmp_list = list()
                tmp_menu['menu'] = value

                for c_key, c_value in data_two.items():
                    if c_value['p_id'] == key:
                        tmp_list.append(c_value)
                tmp_menu['children'] = tmp_list
                data_list.append(tmp_menu)

            roles = Role.objects.prefetch_related('permissions').all()

            paginator = Paginator(roles, settings.PAGE_COUNT)
            obj_page = paginator.page(1)

            context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
            context = {'data': obj_page, 'count': len(roles), 'permissions': data_list}
            context.update(context_data)

            return render(request, 'user/rms_user_role.html', context=context)
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="404")

    def post(self, request):
        name = request.POST.get('name')
        permission_list = request.POST.getlist('permissions')

        if not name:
            return restful.params_error(message="请输入角色名称")
        try:
            role = Role.objects.create(name=name)

            if permission_list:

                permission_tmp = [int(permission) for permission in permission_list]

                permissions = Permission.objects.select_related('menu').all()

                permissions_add = permissions.filter(pk__in=permission_tmp)
                if permissions_add:
                    for permission in permissions_add:
                        p_id = 0
                        if permission.parent:
                            p_id = permission.parent.id
                        if p_id not in permission_tmp:
                            permission_tmp.append(p_id)

                    permissions_add = permissions.filter(id__in=permission_tmp)

                    role.permissions.add(*permissions_add)

            return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="添加权限失败，请刷新数据重试")

    def put(self, request):
        data = QueryDict(request.body)
        try:
            cur_id = int(data.get("cur_id", 0))
        except:
            cur_id = 0

        name = data.get('name')

        permission_list = data.getlist('permissions')

        if not cur_id or not name:
            return restful.params_error(message="请输入角色名称")

        try:
            role = Role.objects.get(id=cur_id)

            permission_tmp = [int(permission) for permission in permission_list]

            permissions = role.permissions.all()

            exist_permissions = []
            for permission in permissions:
                if permission.id not in permission_tmp:
                    role.permissions.remove(permission)
                    for p in permissions:
                        if p.parent:
                            if p.parent.id == permission.id:
                                role.permissions.remove(p)
                else:
                    exist_permissions.append(permission.id)

            update_permissions = list(set(permission_tmp).difference(set(exist_permissions)))

            permissions_add = Permission.objects.select_related('menu').filter(id__in=update_permissions)
            for permission in permissions_add:
                if permission.parent:
                    if permission.parent.id not in update_permissions:
                        update_permissions.append(permission.parent.id)

            permissions_add = Permission.objects.select_related('menu').filter(id__in=update_permissions)

            role.permissions.add(*permissions_add)

            role.name = name
            role.save()

            return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="角色不存在，请刷新数据重试")

    def delete(self, request):
        data = QueryDict(request.body)
        cur_id = data.get("cur_id")

        if not cur_id:
            return restful.params_error(message="角色不存在， 请刷新页面重试")

        try:
            Role.objects.get(id=cur_id).delete()
            return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.params_error(message="角色不存在， 请刷新页面重试")


class RoleListView(View):
    def get(self, request):
        try:
            page = int(request.GET.get('p', 1))
        except:
            page = 1

        # 一页显示多少条数据
        one_page_count = settings.PAGE_COUNT
        start = (page - 1) * one_page_count
        end = start + one_page_count

        roles = Role.objects.all()

        # 总共有多少条数据
        count = len(roles)
        # 一页数据
        data = roles[start:end]
        # 序列化
        serializer = RoleSerializers(data, many=True)
        # 序列化后的数据
        tmp_data = serializer.data

        return restful.result(data={"data": tmp_data, "count": count, "page_count": one_page_count})
