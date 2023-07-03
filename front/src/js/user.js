function User() {
    this.imageCodeId = '';
    this.page = 0;
}

// 生成图片验证码
User.prototype.generateImageCode = function () {
    var self = this;
    var preImageCodeId = self.imageCodeId;
    // 新的要请求的图片验证码的编号
    self.imageCodeId = common.generateUUID();

    $("#get-vercode").attr('src', '/account/captcha/?p=' + preImageCodeId + '&c=' + self.imageCodeId);
};

// 图片验证码更新
User.prototype.captchaUpdateEvent = function () {
    var self = this;

    $("#get-vercode").click(function () {
        self.generateImageCode();
    });
};

// 登录
User.prototype.loginEvent = function () {
    var self = this;

    $("#login-submit").click(function () {
        var username = $("#login-username").val();
        var password = $("#login-password").val();
        var captcha = $("#login-vercode").val();

        if (!username) {
            layer.msg("请输入用户名", {icon: 2, time: 1000});
            return null;
        }
        if (!password) {
            layer.msg("请输入密码", {icon: 2, time: 1000});
            return null;
        }
        if (!captcha) {
            layer.msg("请输入验证码", {icon: 2, time: 1000});
            return null;
        }

        rmsajax.post({
            'url': '/account/login/',
            'data': {
                'password': password,
                'username': username,
                'captcha': captcha,
                'captcha_id': self.imageCodeId
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg("登录成功", {icon: 1, time: 1000}, function () {
                        var next_url = common.getUrlParam("next");
                        if (next_url) {
                            window.location.href = next_url;
                        } else {
                            window.location.href = '/';
                        }
                    });
                }
            }
        });
    });
};


User.prototype.refreshEvent = function () {
    var self = this;
    self.paginatorBtnEvent();
    self.userEditEvent();
    self.userDeleteEvent();
    self.chpwdEvent();
};


// 分页
User.prototype.paginatorBtnEvent = function () {
    var self = this;

    var pageBtn = $(".page-btn");
    pageBtn.unbind('click');
    pageBtn.bind('click', function () {
        var p = $(this).attr('data-p');
        if (!p) {
            p = 1;
        }
        rmsajax.get({
            'url': '/account/userlist/',
            'data': {
                'p': p
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("rms-user-tpl", {"data": data['data']});
                    var tab = $("#rms-user-data");
                    tab.empty();
                    tab.append(tpl);

                    var count = data['count']; // 总共有多少条数据
                    var page_count = data['page_count'];  // 一页显示多少条数据

                    var context = common.paginationHandle(2, parseInt(p), page_count, count);
                    tpl = template("page-item", context);
                    var page_box = $("#rms-user-page");
                    page_box.empty();
                    page_box.append(tpl);
                    $("#user-total_count").text(count);
                    self.refreshEvent();
                }
            }
        });
    });
};


// 添加用户
User.prototype.createUserEvent = function () {
    var self = this;

    $("#rms-add-user").click(function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-add-user-form").reset();
        // 弹框
        layer.open({
            title: '添加用户',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-add-user-tan')
        });
    });

    // 提交表单
    $("#rms-add-user-submit").click(function () {
        var username = $("#rms-add-user-username").val();
        var password1 = $("#rms-add-user-password-1").val();
        var password2 = $("#rms-add-user-password-2").val();
        var user_desc = $("#rms-add-user-desc").val();
        var activation = $("input[name='user-status']:checked").val();
        var roles = $("input[name='add-user-role']:checked");
        var group = $("input[name='add-user-group']:checked").val();
        var roleList = [];

        roles.each(function () {
            var thisInput = $(this);
            roleList.push(thisInput.val());

        });

        if (!username) {
            layer.msg("请输入用户名", {icon: 2, time: 1000});
            return null;
        }
        if (!password1 && !password2) {
            layer.msg("请输入密码", {icon: 2, time: 1000});
            return null;
        } else if (password1 !== password2) {
            layer.msg("两次输入的密码不一致", {icon: 2, time: 1000});
            return null;
        }

        layer.closeAll();
        rmsajax.post({
            'url': '/account/user/',
            'traditional': true,
            'data': {
                'username': username,
                'password1': password1,
                'password2': password2,
                'activation': activation,
                'user_desc': user_desc,
                'roles': roleList,
                'group': group
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg("创建用户成功", {icon: 1, time: 1000}, function () {
                        window.location = window.location.href;
                    });
                }
            }
        });
    });
};

// 编辑
User.prototype.userEditEvent = function () {
    var self = this;
    var usernameDiv = $("#rms-edit-user-username");
    var userDescInput = $("#rms-edit-user-desc");
    var rmsEditUserSubmitBtn = $("#rms-edit-user-submit");
    var id = 0;
    var rmsEditUserBtn = $(".rms-edit-user-btn");
    rmsEditUserBtn.unbind('click');
    rmsEditUserBtn.bind('click', function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-edit-user-form").reset();
        var par = $(this).parent('td');
        id = par.attr("data-value");

        var roles = par.attr("data-r");

        var group = par.prevAll('.user-group').attr('data-value');
        $("input[name='edit-user-group'][value='" + group + "']").prop('checked', true);

        $.each(roles.split(','), function (index, value) {
            if (value) {
                $("input[name='edit-user-role'][value='" + value + "']").prop('checked', true);
            }
        });
        // user-edit-status
        var r_value = par.prevAll('.user-is_active').attr('data-value');

        $("input[name='user-edit-status'][value='" + r_value + "']").prop('checked', true);

        usernameDiv.text(par.prevAll('.user-username').text());
        userDescInput.val(par.prevAll('.user-user_desc').text());

        layui.form.render();

        // 弹框
        layer.open({
            title: '编辑用户',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-edit-user-tan')
        });
    });
    rmsEditUserSubmitBtn.unbind('click');
    rmsEditUserSubmitBtn.bind('click', function () {
        var self = this;

        var user_desc = $("#rms-edit-user-desc").val();
        var activation = $("input[name='user-edit-status']:checked").val();
        var roles = $("input[name='edit-user-role']:checked");
        var group = $("input[name='edit-user-group']:checked").val();
        var roleList = [];

        roles.each(function () {
            var thisInput = $(this);
            roleList.push(thisInput.val());
        });

        if (!id) {
            layer.msg("编辑的用户不存在，请刷新页面重试！", {icon: 2, time: 1000});
            return null;
        }

        layer.closeAll();
        rmsajax.put({
            'url': '/account/user/',
            'traditional': true,
            'data': {
                // 'username': username,
                'activation': activation,
                'user_desc': user_desc,
                'roles': roleList,
                'user_id': id,
                'group': group
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg("用户编辑成功", {icon: 1, time: 1000}, function () {
                        window.location = window.location.href;
                    });
                }
            }
        });

    });
};

// 删除用户
User.prototype.userDeleteEvent = function () {
    var self = this;
    var rmsDeleteUserBtn = $(".rms-delete-user-btn");
    rmsDeleteUserBtn.unbind('click');
    rmsDeleteUserBtn.bind('click', function () {
        var id = $(this).parent('td').attr("data-value");

        layer.confirm('确定要删除？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (id) {
                rmsajax.delete({
                    "url": '/account/user/',
                    'data': {
                        "user_id": id
                    }, "success": function (result) {
                        if (result['code'] === 200) {
                            layer.msg("用户删除成功", {icon: 1, time: 1000}, function () {
                                window.location = window.location.href;
                            });
                        }
                    }
                });
            } else {
                layer.msg("用户不存在， 请刷新数据重试", {icon: 2, time: 2000});
            }
        }, function () { // 第二个按钮事件回调
            layer.closeAll(); // 关闭对话框
        });
    });
};

// 修改其他用户密码
User.prototype.chpwdEvent = function () {
    var self = this;
    var id = 0;

    var rmsChpwdUserBtn = $(".rms-chpwd-user-btn");
    rmsChpwdUserBtn.unbind('click');
    rmsChpwdUserBtn.bind('click', function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-chpwd-user-form").reset();
        var par = $(this).parent('td');
        id = par.attr('data-value');
        $("#rms-chpwd-user-username").text(par.prevAll('.user-username').text());
        // 弹框
        layer.open({
            title: '修改用户密码',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-chpwd-user-tan')
        });
    });

    var chpwdSubmit = $("#rms-chpwd-user-submit");
    chpwdSubmit.unbind('click');
    chpwdSubmit.bind('click', function () {
        if (!id) {
            layer.msg("用户不存在， 请刷新数据重试", {icon: 2, time: 2000});
        }
        var pwd1 = $("#rms-chpwd-user-password-1").val();
        var pwd2 = $("#rms-chpwd-user-password-2").val();
        if (!pwd1 || !pwd2 || pwd1 !== pwd2) {
            layer.msg("两次输入的密码不一致", {icon: 2, time: 2000});
        }

        layer.closeAll();
        rmsajax.post({
            "url": "/account/chpwd/",
            "data": {
                'user_id': id,
                'password1': pwd1,
                'password2': pwd2
            },
            "success": function (result) {
                if (result['code'] === 200) {
                    layer.msg("修改密码成功", {icon: 1, time: 1000});
                }
            }
        });

    });
};

// 修改当前用户密码
User.prototype.currentChpwdEvent = function () {
    var self = this;
    // var id = 0;

    var rmsChpwdUserBtn = $("#current-chpwd-btn");
    rmsChpwdUserBtn.unbind('click');
    rmsChpwdUserBtn.bind('click', function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-chpwd-user-form").reset();
        // var par = $(this).parent('td');
        // id = par.attr('data-value');
        // $("#rms-chpwd-user-username").text(par.prevAll('.user-username').text());
        // 弹框
        layer.open({
            title: '修改当前登录用户密码',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-chpwd-user-tan')
        });
    });

    var chpwdSubmit = $("#rms-chpwd-user-submit");
    chpwdSubmit.unbind('click');
    chpwdSubmit.bind('click', function () {
        // if (!id){
        //     layer.msg("用户不存在， 请刷新数据重试", {icon: 2, time: 2000});
        // }
        var pwd1 = $("#rms-chpwd-user-password-1").val();
        var pwd2 = $("#rms-chpwd-user-password-2").val();
        if (!pwd1 || !pwd2 || pwd1 !== pwd2) {
            layer.msg("两次输入的密码不一致", {icon: 2, time: 2000});
        }

        layer.closeAll();
        rmsajax.put({
            "url": "/account/chpwd/",
            "data": {
                // 'user_id': id,
                'password1': pwd1,
                'password2': pwd2
            },
            "success": function (result) {
                if (result['code'] === 200) {
                    layer.msg("修改密码成功", {icon: 1, time: 1000}, function () {
                        window.location.href = "/account/logout/";
                    });
                }
            }
        });
    });
};


User.prototype.run = function () {
    // this.generateImageCode();
    // this.captchaUpdateEvent();
    // this.loginEvent();
    this.paginatorBtnEvent();
    this.createUserEvent();
    this.userEditEvent();
    this.userDeleteEvent();
    this.chpwdEvent();
};


function Role() {
    this.page = 1;
}

Role.prototype.refreshEvent = function () {
    var self = this;
    self.roleEditEvent();
    self.roleDeleteEvent();
    self.paginatorBtnEvent();
};

// 分页
Role.prototype.paginatorBtnEvent = function () {
    var self = this;
    var pageBtn = $(".page-btn");
    pageBtn.unbind("click");
    pageBtn.bind("click", function () {
        var p = $(this).attr('data-p');
        if (!p) {
            p = 1;
        }
        rmsajax.get({
            'url': '/account/rolelist/',
            'data': {
                'p': p
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("rms-user-role-tpl", {"data": data['data']});
                    var tab = $("#rms-user-role-data");
                    tab.empty();
                    tab.append(tpl);

                    var count = data['count']; // 总共有多少条数据
                    var page_count = data['page_count'];  // 一页显示多少条数据

                    var context = common.paginationHandle(2, parseInt(p), page_count, count);
                    tpl = template("page-item", context);
                    var page_box = $("#rms-user-role-page");
                    page_box.empty();
                    page_box.append(tpl);
                    $("#user-role-total_count").text(count);
                    self.refreshEvent();
                }
            }
        });
    });
};

// 添加角色
Role.prototype.roleAddEvent = function () {
    var self = this;

    $("#rms-add-user-role").click(function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-add-user-role-form").reset();
        // 弹框
        layer.open({
            title: '添加角色',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-add-user-role-tan')
        });
    });

    $("#rms-add-user-role-submit").click(function () {
        var title = $("#rms-add-user-role-name").val();
        var permissionList = [];

        $("input[name='add-permission']").each(function () {
            var thisInput = $(this);

            if (thisInput.prop('checked')) {
                permissionList.push(thisInput.val());
            }
        });

        if (title) {
            layer.closeAll();
            rmsajax.post({
                'url': '/account/role/',
                'traditional': true,
                'data': {
                    'name': title,
                    'permissions': permissionList
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        layer.msg("添加角色成功", {icon: 1, time: 1000}, function () {
                            window.location = window.location.href;
                        });
                    }
                }
            });
        } else {
            layer.msg("请输入角色名称", {icon: 2, time: 2000});
        }
    });
};

// 编辑角色
Role.prototype.roleEditEvent = function () {
    var self = this;
    var par;
    var id = 0;
    var rmsEditRoleBtn = $("#rms-edit-user-role-submit");
    var roleNameInput = $("#rms-edit-user-role-name");

    var rmsEditRole = $(".rms-edit-user-role");
    rmsEditRole.unbind('click');
    rmsEditRole.bind('click', function () {
        document.getElementById("rms-edit-user-role-form").reset();
        par = $(this).parent('td');
        id = par.attr("data-value");
        // 初始化表单
        var permissions = par.attr("data-p");

        $.each(permissions.split(','), function (index, value) {
            if (value) {
                $("input[name='edit-permission'][value='" + value + "']").prop('checked', true);
            }
        });
        roleNameInput.val(par.prevAll('.role-name').text());

        layui.form.render();

        // 弹框
        layer.open({
            title: '添加角色',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-edit-user-role-tan')
        });
    });

    rmsEditRoleBtn.unbind("click");
    rmsEditRoleBtn.bind("click", function () {
        var title = $("#rms-edit-user-role-name").val();
        var permissionList = [];

        $("input[name='edit-permission']").each(function () {
            var thisInput = $(this);

            if (thisInput.prop('checked')) {
                permissionList.push(thisInput.val());
            }
        });

        if (!title) {
            layer.msg("请输入角色名称", {icon: 2, time: 2000});
            return null;
        }

        layer.closeAll();
        rmsajax.put({
            'url': '/account/role/',
            'traditional': true,
            'data': {
                'cur_id': id,
                'name': title,
                'permissions': permissionList
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg("修改角色成功", {icon: 1, time: 1000}, function () {
                        window.location = window.location.href;
                    });
                }
            }
        });
    });
};

// 删除角色
Role.prototype.roleDeleteEvent = function () {
    var self = this;
    var rmsDeleteRole = $(".rms-delete-user-role");
    rmsDeleteRole.unbind('click');
    rmsDeleteRole.bind('click', function () {
        var id = $(this).parent('td').attr("data-value");

        layer.confirm('确定要删除？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (id) {
                rmsajax.delete({
                    "url": '/account/role/',
                    'data': {
                        "cur_id": id
                    }, "success": function (result) {
                        if (result['code'] === 200) {
                            layer.msg("删除角色成功", {icon: 1, time: 1000}, function () {
                                window.location = window.location.href;
                            });
                        }
                    }
                });
            } else {
                layer.msg("角色不存在， 请刷新数据重试", {icon: 2, time: 2000});
            }
        }, function () { // 第二个按钮事件回调
            layer.closeAll(); // 关闭对话框
        });
    });
};

Role.prototype.run = function () {
    this.roleAddEvent();
    this.roleEditEvent();
    this.roleDeleteEvent();
    this.paginatorBtnEvent();
};


function Group() {

}

// 刷新事件
Group.prototype.refreshEvent = function () {
    var self = this;
    self.paginatorBtnEvent();
    self.editUserGroupEvent();
    self.groupDeleteEvent();
};

// 分页处理
Group.prototype.paginatorBtnEvent = function () {
    var self = this;
    var pageBtn = $(".page-btn");
    pageBtn.unbind("click");
    pageBtn.bind("click", function () {
        var p = $(this).attr('data-p');
        if (!p) {
            p = 1;
        }
        rmsajax.get({
            'url': '/account/usergrouplist/',
            'data': {
                'p': p
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("rms-user-group-tpl", {"data": data['data']});
                    var tab = $("#rms-user-group-data");
                    tab.empty();
                    tab.append(tpl);

                    var count = data['count']; // 总共有多少条数据
                    var page_count = data['page_count'];  // 一页显示多少条数据

                    var context = common.paginationHandle(2, parseInt(p), page_count, count);
                    tpl = template("page-item", context);
                    var page_box = $("#rms-user-group-page");
                    page_box.empty();
                    page_box.append(tpl);
                    $("#user-group-total_count").text(count);
                    self.refreshEvent();
                }
            }
        });
    });
};

// 添加用户组
Group.prototype.addUserGroupEvent = function () {
    var self = this;
    var addUserGroupBtn = $("#rms-add-user-group");
    addUserGroupBtn.unbind('click');
    addUserGroupBtn.bind('click', function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-add-user-group-form").reset();
        // 弹框
        layer.open({
            title: '添加用户组',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-add-user-group-tan')
        });
    });

    var addSubmit = $("#rms-add-user-group-submit");
    addSubmit.unbind('click');
    addSubmit.bind('click', function () {
        var groupname = $("#rms-add-user-group-name").val();
        if (!groupname) {
            layer.msg("请输入用户组名", {icon: 2, time: 2000});
        }

        layer.closeAll();
        rmsajax.post({
            'url': '/account/usergroup/',
            'data': {
                'groupname': groupname
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg("用户组添加成功", {icon: 1, time: 1000}, function () {
                        window.location = window.location.href;
                    });
                }
            }
        });
    });
};

// 编辑用户组
Group.prototype.editUserGroupEvent = function () {
    var id = 0;
    var titleInput = $("#rms-edit-user-group-name");
    var rmsEditUserGroupBtn = $(".rms-edit-user-group");
    rmsEditUserGroupBtn.unbind('click');
    rmsEditUserGroupBtn.bind('click', function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-edit-user-group-form").reset();
        var par = $(this).parent('td');
        id = par.attr("data-value");
        titleInput.val(par.prevAll('td.group-title').text());
        // 弹框
        layer.open({
            title: '修改用户组',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-edit-user-group-tan')
        });
    });

    var editGroupBtn = $("#rms-edit-user-group-submit");
    editGroupBtn.unbind('click');
    editGroupBtn.bind('click', function () {
        var title = titleInput.val();
        if (!id || !title) {
            layer.msg("请输入用户组名", {icon: 2, time: 2000});
        }

        layer.closeAll();
        rmsajax.put({
            'url': '/account/usergroup/',
            'data': {
                'group_id': id,
                'title': title
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg("编辑用户组成功", {icon: 1, time: 1000}, function () {
                        window.location = window.location.href;
                    });
                }
            }
        });
    });
};

// 删除角色
Group.prototype.groupDeleteEvent = function () {
    var self = this;
    var rmsDeleteGroup = $(".rms-delete-user-group");
    rmsDeleteGroup.unbind('click');
    rmsDeleteGroup.bind('click', function () {
        var id = $(this).parent('td').attr("data-value");

        layer.confirm('确定要删除？', {
            btn: ['确定', '取消'] //按钮
        }, function () { // 第一个按钮事件回调
            if (id) {
                rmsajax.delete({
                    "url": '/account/usergroup/',
                    'data': {
                        'group_id': id
                    }, "success": function (result) {
                        if (result['code'] === 200) {
                            layer.msg("用户组删除成功", {icon: 1, time: 1000}, function () {
                                window.location = window.location.href;
                            });
                        }
                    }
                });
            } else {
                layer.msg("用户组不存在， 请刷新数据重试", {icon: 2, time: 2000});
            }
        }, function () { // 第二个按钮事件回调
            layer.closeAll(); // 关闭对话框
        });
    });
};

Group.prototype.run = function () {
    this.addUserGroupEvent();
    this.paginatorBtnEvent();
    this.editUserGroupEvent();
    this.groupDeleteEvent();
};