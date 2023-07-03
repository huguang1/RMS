import logging
from django.shortcuts import render
from django.views import View
from django.http import QueryDict
from django.conf import settings

from utils import restful, add_logs, wu_paginator

from apps.rmsManager import forms
from apps.rmsManager import models
from apps.rmsauth.models import User

logger = logging.getLogger("django")


class RecruitmentWayView(View):
    """
    rw:RecruitmentWay的缩写
    """

    def get(self, request, pk=0):
        if not pk:
            try:
                current_page = int(request.GET.get("p"))
            except Exception as e:
                current_page = 1
            rw_obj_list = models.RecruitmentWay.objects.all()
            posts = wu_paginator.WuPaginator(current_page, settings.MAX_PAGE_NUM, rw_obj_list,
                                             settings.PER_PAGE).get_paginator()
            return render(request, "manage/rwList.html", {"posts": posts})

        rw_obj_list = models.RecruitmentWay.objects.filter(pk=pk)
        if not rw_obj_list:
            return restful.params_error("你所选择的招聘渠道不存在")

        rw = rw_obj_list[0]
        return render(request, "manage/rw.html", {"rw": rw})

    def post(self, request, pk=0):
        form = forms.RecruitmentWayForm(request.POST)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())

        name = form.cleaned_data.get("name")
        link_man = form.cleaned_data.get("link_man")
        contact_way = form.cleaned_data.get("contact_way")

        if models.RecruitmentWay.objects.filter(name=name):
            return restful.params_error("你所添加的渠道名已存在")

        try:
            models.RecruitmentWay.objects.create(name=name, link_man=link_man, contact_way=contact_way)
        except Exception as e:
            logger.error(e)
            return restful.server_error("渠道创建失败,服务器异常")

        add_logs.add_log("创建渠道", f"创建渠道{name}", request.user)
        return restful.ok()

    def put(self, request, pk=0):
        rw_obj_list = models.RecruitmentWay.objects.filter(pk=pk)
        if not rw_obj_list:
            return restful.params_error("你所修改的渠道不存在")

        put = QueryDict(request.body)
        form = forms.RecruitmentWayForm(put)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())

        name = form.cleaned_data.get("name")
        link_man = form.cleaned_data.get("link_man")
        contact_way = form.cleaned_data.get("contact_way")

        try:
            rw_obj_list.update(name=name, link_man=link_man, contact_way=contact_way)
        except Exception as e:
            logger.error(e)
            return restful.server_error("渠道信息修改失败,服务器异常")

        add_logs.add_log("编辑渠道", f"编辑渠道{name}", request.user)
        return restful.ok()

    def delete(self, request, pk=0):
        rw_obj_list = models.RecruitmentWay.objects.filter(pk=pk)
        if not rw_obj_list:
            return restful.params_error("你所删除的岗位不存在")

        try:
            name = rw_obj_list[0].name
            rw_obj_list.delete()
        except Exception as e:
            logger.error(e)
            return restful.server_error("渠道信息删除失败,服务器异常")

        add_logs.add_log("删除渠道", f"删除渠道{name}", request.user)
        return restful.ok()