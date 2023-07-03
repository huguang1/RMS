/*
@author: 技术-小明
@time: 2019-04-19 15:17:58
@file: develop.html
@desc:
*/

function Menu() {
    this.page = 1;
}

Menu.prototype.refreshEvent = function () {
    this.paginatorBtnEvent();
    this.menuDeleteEvent();
    this.menuEditEvent();
};


// 分页按钮
Menu.prototype.paginatorBtnEvent = function () {
    var self = this;

    $(".page-btn").click(function () {
        var p = $(this).attr('data-p');

        if (p) {
            self.page = p;
            rmsajax.get({
                "url": '/account/menulist/',
                "data": {
                    'p': p
                },
                "success": function (result) {
                    if (result['code'] === 200) {
                        var data = result['data'];
                        var tpl = template("rms-user-menu-tpl", {"data": data['data']});
                        var tab = $("#rms-user-menu-data");
                        tab.empty();
                        tab.append(tpl);

                        var count = data['count']; // 总共有多少条数据
                        var page_count = data['page_count'];  // 一页显示多少条数据

                        var context = common.paginationHandle(2, parseInt(p), page_count, count);
                        tpl = template("page-item", context);
                        var page_box = $("#rms-user-menu-page");
                        page_box.empty();
                        page_box.append(tpl);
                        $("#user-menu-total_count").text(count);
                        self.refreshEvent();
                    }
                }
            });
        }
    });
};

// 添加菜单
Menu.prototype.menuAddEvent = function () {
    $("#rms-add-user-menu").click(function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-add-user-menu-form").reset();
        // 弹框
        layer.open({
            title: '添加菜单',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-add-user-menu-tan')
        });
    });

    $("#rms-add-user-menu-submit").click(function () {
        var name = $("#rms-add-user-menu-name").val();
        layer.closeAll();
        rmsajax.post({
            "url": "/account/menu/",
            "data": {
                'name': name
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg("添加菜单成功", {icon: 1, time: 1000}, function () {
                        window.location = window.location.href;
                    });
                }
            }
        });
    });
};

// 删除菜单
Menu.prototype.menuDeleteEvent = function () {
    $(".rms-delete-user-menu").click(function () {
        var id = $(this).attr('data-id');

        layer.confirm('确定要删除？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (id) {
                rmsajax.delete({
                    'url': '/account/menu/',
                    'data': {
                        'id': id
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            layer.msg("删除菜单成功", {icon: 1, time: 1000}, function () {
                                window.location = window.location.href;
                            });
                        }
                    }
                });
            } else {
                layer.msg("删除菜单失败, 请刷新数据重试", {icon: 1, time: 2000}, function () {
                    window.location = window.location.href;
                });
            }
        }, function () { // 第二个按钮事件回调
            layer.closeAll(); // 关闭对话框
        });
    });
};

// 编辑菜单
Menu.prototype.menuEditEvent = function () {
    var menuInput = $("#rms-edit-user-menu-title");
    var id = 0;

    $(".rms-edit-user-menu").click(function () {
        id = $(this).attr("data-id");
        var prt = $(this).parent('td');
        menuInput.val(prt.prevAll('.menu-title').text());
        // 初始化表单, 清空表单数据
        // document.getElementById("rms-edit-user-menu-form").reset();

        // 弹框
        layer.open({
            title: '添加菜单',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-edit-user-menu-tan')
        });
    });

    $("#rms-edit-user-menu-submit").click(function () {
        var title = menuInput.val();
        layer.closeAll();
        rmsajax.put({
            'url': '/account/menu/',
            'data': {
                'id': id,
                'title': title
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg("编辑菜单成功", {icon: 1, time: 1000}, function () {
                        window.location = window.location.href;
                    });
                }
            }
        });
    });
};


Menu.prototype.run = function () {
    this.menuAddEvent();
    this.menuDeleteEvent();
    this.menuEditEvent();
    this.paginatorBtnEvent();
};


function Permission() {
    this.page = 1;
}

// 分页
Permission.prototype.paginatorBtnEvent = function () {
    var self = this;
    var pageBtn = $(".page-btn");
    pageBtn.unbind("click");
    pageBtn.bind("click", function () {
        var p = $(this).attr('data-p');

        if (p) {
            self.page = p;
            rmsajax.get({
                "url": '/account/permissionlist/',
                "data": {
                    'p': p
                },
                "success": function (result) {
                    if (result['code'] === 200) {
                        var data = result['data'];
                        var tpl = template("rms-user-permission-tpl", {"data": data['data']});
                        var tab = $("#rms-user-permission-data");
                        tab.empty();
                        tab.append(tpl);

                        var count = data['count']; // 总共有多少条数据
                        var page_count = data['page_count'];  // 一页显示多少条数据

                        var context = common.paginationHandle(2, parseInt(p), page_count, count);
                        tpl = template("page-item", context);
                        var page_box = $("#rms-user-permission-page");
                        page_box.empty();
                        page_box.append(tpl);
                        $("#user-permission-total_count").text(count);
                        // self.refreshEvent();
                        self.paginatorBtnEvent();
                        self.permissionEditEvent();
                        self.permissionDeleteEvent();
                    }
                }
            });
        }
    });
};


// 添加权限
Permission.prototype.permissionAddEvent = function () {
    var self = this;

    $("#rms-add-user-permission").click(function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-add-user-permission-form").reset();
        // 弹框
        layer.open({
            title: '添加权限',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-add-user-permission-tan')
        });
    });

    $("#rms-add-user-permission-submit").click(function () {
        var title = $("#rms-add-user-permission-name").val();
        var url = $("#rms-add-user-permission-url").val();
        var parentInput = $("input[name='parent']:checked");
        var parentType = parentInput.attr('data-type');
        var parentValue = parentInput.val();
        var method = $("input[name='method']:checked").val();
        // $("input[name='parent'][data-type='1'][value='14']").prop("checked", true);
        // layui.form.render(); //重新渲染

        if (title && url && parentType && parentValue && method) {
            layer.closeAll();
            rmsajax.post({
                'url': '/account/permission/',
                'data': {
                    'title': title,
                    'url': url,
                    'p_type': parentType,
                    'p_id': parentValue,
                    'method': method
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.msg("权限添加成功！", {icon: 1, time: 1000}, function () {
                            // self.refreshCurrentPage();
                            window.location = window.location.href;
                        });
                    }
                }
            });
        } else {
            layer.msg("请输入正确的参数", {icon: 2, time: 2000});
        }
    });
};

// 编辑权限
Permission.prototype.permissionEditEvent = function () {
    var self = this;
    var id;
    var prt;
    var titleInput = $("#rms-edit-user-permission-name");
    var urlInput = $("#rms-edit-user-permission-url");

    var submitBtn = $("#rms-edit-user-permission-submit");
    submitBtn.unbind('click');

    $(".rms-edit-user-permission").click(function () {
        // 表单初始化
        prt = $(this).parent('td');
        id = prt.attr("data-value");
        titleInput.val(prt.prevAll('.permission-title').text());
        urlInput.val(prt.prevAll('.permission-url').text());
        var td_method = prt.prevAll('.permission-method').text();
        $("input[name='edit-method'][value='" + td_method + "']").prop("checked", true);
        var parentTmp = prt.prevAll('.permission-parent');
        var type = parentTmp.attr('data-type');
        var value = parentTmp.attr('data-value');
        $("input[name='edit-parent'][data-type='" + type + "'][value='" + value + "']").prop("checked", true);
        // 禁用当前编辑的权限
        $("input[name='edit-parent']").prop('disabled', false);
        var curInput = $("input[name='edit-parent'][data-type='0'][value='" + id + "']");
        if (curInput) {
            curInput.prop('disabled', true).siblings().prop('disabled', false);
        }
        // 刷新表单显示
        layui.form.render();

        // 弹框
        layer.open({
            title: '编辑权限',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-edit-user-permission-tan')
        });
    });


    submitBtn.bind('click', function () {
        var title = titleInput.val();
        var url = urlInput.val();
        var parentInput = $("input[name='edit-parent']:checked");
        var parentType = parentInput.attr('data-type');
        var parentValue = parentInput.val();
        var method = $("input[name='edit-method']:checked").val();

        if (title && url && parentType && parentValue && method && id) {
            layer.closeAll();
            rmsajax.put({
                'url': '/account/permission/',
                'data': {
                    'title': title,
                    'url': url,
                    'p_type': parentType,
                    'p_id': parentValue,
                    'method': method,
                    'cur_id': id
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.msg("权限编辑成功！", {icon: 1, time: 1000}, function () {
                            window.location = window.location.href;
                        });
                    }
                }
            });
        } else {
            layer.msg("请输入正确的参数", {icon: 2, time: 2000});
        }
    });
};

// 删除权限
Permission.prototype.permissionDeleteEvent = function () {
    var self = this;

    var deleteBtn = $(".rms-delete-user-permission");
    deleteBtn.unbind('click');

    deleteBtn.bind('click', function () {
        var id = $(this).parent('td').attr("data-value");

        layer.confirm('确定要删除？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (id) {
                rmsajax.delete({
                    "url": '/account/permission/',
                    'data': {
                        "cur_id": id
                    }, "success": function (result) {
                        if (result['code'] === 200) {
                            layer.msg("删除权限成功", {icon: 1, time: 1000}, function () {
                                window.location = window.location.href;
                            });
                        }
                    }
                });
            } else {
                layer.msg("删除权限失败， 请刷新数据重试", {icon: 2, time: 2000});
            }
        }, function () { // 第二个按钮事件回调
            layer.closeAll(); // 关闭对话框
        });
    });
};


Permission.prototype.run = function () {
    this.permissionAddEvent();
    this.paginatorBtnEvent();
    this.permissionEditEvent();
    this.permissionDeleteEvent();
};
