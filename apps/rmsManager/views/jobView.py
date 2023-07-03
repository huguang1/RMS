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


class JobView(View):

    def get(self, request, pk=0):
        if not pk:
            try:
                current_page = int(request.GET.get("p"))
            except Exception as e:
                current_page = 1
            job_obj_list = models.Job.objects.all().order_by("id")
            posts = wu_paginator.WuPaginator(current_page, settings.MAX_PAGE_NUM, job_obj_list,
                                             settings.PER_PAGE).get_paginator()
            return render(request, "manage/jobList.html", {"posts": posts})

        job_obj_list = models.Job.objects.filter(pk=pk)
        if not job_obj_list:
            return restful.params_error("你所选择的岗位不存在")

        job = job_obj_list[0]
        return render(request, "manage/job.html", {"job": job})

    def post(self, request, pk=0):
        form = forms.JobFrom(request.POST)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())

        name = form.cleaned_data.get("name")
        if models.Job.objects.filter(name=name):
            return restful.params_error("你所添加的岗位已存在")

        try:
            models.Job.objects.create(name=name)
        except Exception as e:
            logger.error(e)
            return restful.server_error("岗位创建失败,服务器异常")

        add_logs.add_log("创建岗位", f"创建岗位{name}", request.user)
        return restful.ok()



    def put(self, request, pk=0):
        job_obj_list = models.Job.objects.filter(pk=pk)
        if not job_obj_list:
            return restful.params_error("你所修改的岗位不存在")

        put = QueryDict(request.body)
        form = forms.JobFrom(put)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())

        name = form.cleaned_data.get("name")
        try:
            job_obj_list.update(name=name)
        except Exception as e:
            logger.error(e)
            return restful.server_error("岗位信息修改失败,服务器异常")

        add_logs.add_log("编辑岗位", f"编辑岗位{name}", request.user)
        return restful.ok()


    def delete(self, request, pk=0):
        job_obj_list = models.Job.objects.filter(pk=pk)
        if not job_obj_list:
            return restful.params_error("你所删除的岗位不存在")

        try:
            name = job_obj_list[0].name
            job_obj_list.delete()
        except Exception as e:
            logger.error(e)
            return restful.server_error("岗位信息删除失败,服务器异常")

        add_logs.add_log("删除岗位", f"删除岗位{name}", request.user)
        return restful.ok()