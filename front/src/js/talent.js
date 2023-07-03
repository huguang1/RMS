function Talent() {

}

// 刷新事件
Talent.prototype.refreshEvent = function () {
    var self = this;
    self.paginatorBtnEvent();
};

// 人才信息页面 分页
Talent.prototype.paginatorBtnEvent = function () {
    var self = this;
    var pageBtn = $(".page-btn");
    pageBtn.unbind("click");
    pageBtn.bind("click", function () {
        var p = $(this).attr('data-p');
        if (!p) {
            p = 1;
        }
        rmsajax.get({
            'url': '/talent/talentlist/',
            'data': {
                'p': p
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var tpl = template("rms-talent-tpl", {"data": data['data']});
                    var tab = $("#rms-talent-data");
                    tab.empty();
                    tab.append(tpl);

                    var count = data['count']; // 总共有多少条数据
                    var page_count = data['page_count'];  // 一页显示多少条数据

                    var context = common.paginationHandle(2, parseInt(p), page_count, count);
                    tpl = template("page-item", context);
                    var page_box = $("#rms-talent-page");
                    page_box.empty();
                    page_box.append(tpl);
                    $("#rms-talent-total_count").text(count);
                    self.refreshEvent();
                }
            }
        });
    });
};

// 人才信息录入
Talent.prototype.entryInfoEvent = function () {

    var self = this;

    $("#rms-add-talent").click(function () {
        window.location.href = "/talent/entryinfo/";
    });
};

// 上传简历
Talent.prototype.uploadBtnEvent = function () {
    var uploadTools = $("#upload-tools");
    $("#upload-btn").click(function () {
        uploadTools.click();
    });

    uploadTools.change(function () {
        var file = this.files[0];
        var fileExtension = file.name.split('.').pop().toLowerCase();
        if (fileExtension !== 'pdf') {
            layer.msg("简历必须是PDF格式的文档", {icon: 2, time: 2000});
            return null;
        }
        var formData = new FormData();
        formData.append("file", file);
        rmsajax.post({
            'url': '/talent/upload/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var name = result['data']['name'];
                    $("#upload-name-show").val(name);
                    layer.msg("简历上传成功", {icon: 1, time: 1000});
                }
            }
        });
    });
};

// 添加区域
Talent.prototype.addRegionEvent = function () {
    $("#rms-add-talent-region-btn").click(function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-add-region-form").reset();
        // 弹框
        layer.open({
            title: '添加区域',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-add-region-tan')
        });
    });

    $("#rms-add-region-submit").click(function () {
        var name = $("#rms-add-region-name").val();
        if (!name) {
            layer.msg("请输入区域名称", {icon: 2, time: 2000});
        }

        layer.closeAll();
        rmsajax.post({
            'url': '/talent/region/',
            'data': {
                'name': name
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var html = "<option value=\"" + data['id'] + "\">" + data['name'] + "</option>";
                    $("#rms-add-talent-region").append(html);
                    layui.form.render();
                    layer.msg("区域添加成功", {icon: 1, time: 1000});
                }
            }
        });
    });
};

// 添加应聘过的公司 interviewed
Talent.prototype.addInterviewedEvent = function () {
    $("#rms-add-talent-interviewed").click(function () {
        // 初始化表单, 清空表单数据
        document.getElementById("rms-add-interviewed-form").reset();
        // 弹框
        layer.open({
            title: '添加应聘过的公司',
            type: 1,
            skin: 'layui-layer-rim',
            area: ['600px', ''],
            content: $('#rms-add-interviewed-tan')
        });
    });

    $("#rms-add-interviewed-submit").click(function () {
        var name = $("#rms-add-interviewed-name").val();
        if (!name) {
            layer.msg("请输入公司名称", {icon: 2, time: 2000});
        }

        layer.closeAll();
        rmsajax.post({
            'url': '/talent/interviewed/',
            'data': {
                'name': name
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var data = result['data'];
                    var html = "<input type=\"checkbox\" name=\"interviewed\" title=\"" + data['name'] + "\"value=\"" + data['name'] + "\" lay-skin=\"primary\">"
                    $("#interviewed-checkbox").append(html);
                    layui.form.render();
                    layer.msg("区域添加成功", {icon: 1, time: 1000});
                }
            }
        });
    });
};

// 添加人才 rms-talent-submit
Talent.prototype.addTalentEvent = function () {
    $("#rms-add-talent-submit").click(function () {
        var name = $("#rms-add-talent-name").val();
        var gender = $("#rms-add-talent-gender").val();
        var channel = $("#rms-add-talent-channel").val();
        var region = $("#rms-add-talent-region").val();
        var status = $("#rms-add-talent-status").val();
        var resume_uuid = $("#upload-name-show").val();
        var expectJob = $("input[name='job'][type='checkbox']:checked");
        var arr = new Array();
        expectJob.each(function () {
            var thisInput = $(this);
            arr.push(thisInput.val());
            arr.push(",");
        });
        var expect_str = arr.join("");
        var expect_job = expect_str.substring(0, expect_str.length - 1);

        var interviewedList = [];
        $("input[name='interviewed'][type='checkbox']").each(function () {
            var thisInput = $(this);

            if (thisInput.prop('checked')) {
                interviewedList.push(thisInput.val());
            }
        });
        var remark = $("#rms-add-talent-remark").val();

        if (!name) {
            layer.msg("请输入姓名", {icon: 2, time: 2000});
            return null;
        }
        if (!channel) {
            layer.msg("请选择招聘途径", {icon: 2, time: 2000});
            return null;
        }
        if (!region) {
            layer.msg("请选择区域", {icon: 2, time: 2000});
            return null;
        }
        if (!region) {
            layer.msg("请选择人才状态", {icon: 2, time: 2000});
            return null;
        }
        layer.closeAll();
        rmsajax.post({
            'url': '/talent/entryinfo/',
            'traditional': true,
            'data': {
                'name': name,
                'gender': gender,
                'channel': channel,
                'region': region,
                'status': status,
                'resume_uuid': resume_uuid,
                'expect_job': expect_job,
                'interviewed': interviewedList,
                'remark': remark
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    layer.msg("添加人才成功", {icon: 1, time: 1000}, function () {
                        window.location.href = "/talent/";
                    });
                }
            }
        });
    });
};

Talent.prototype.run = function () {
    this.entryInfoEvent();
    this.addRegionEvent();
    this.uploadBtnEvent();
    this.addInterviewedEvent();
    this.addTalentEvent();
    this.paginatorBtnEvent();
};

$(function () {
    var talent = new Talent();
    talent.run();
});