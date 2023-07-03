"""
@author: 技术-小明
@time: 2019-04-05 19:32:48
@file: init_permission.py
@desc: 初始化权限
"""


def init_permission(request):
    permissions_list = [permission for role in request.user.roles.all() for permission in role.permissions.all()]
    # 一级菜单
    data_one = dict()
    # 二级菜单
    data_two = dict()
    #  权限
    permissions_data = []
    # 菜单 权限
    for permission in list(set(permissions_list)):
        permissions_data.append({'url': permission.url, 'method': permission.method})
        if permission.menu:
            data_one[permission.menu.id] = {'id': permission.menu.id, 'title': permission.menu.title}
            data_two[permission.id] = {'id': permission.id, 'title': permission.title,
                                       'p_id': permission.menu.id, 'url': permission.url}
    menu_data = []
    for key, value in data_one.items():
        tmp_menu = dict()
        tmp_list = list()
        tmp_menu['menu'] = value

        for c_key, c_value in data_two.items():
            if c_value['p_id'] == key:
                tmp_list.append(c_value)
        tmp_menu['children'] = tmp_list
        menu_data.append(tmp_menu)

    request.session["rms_permission_url_list_key"] = permissions_data
    request.session["rms_menu_list_key"] = menu_data
