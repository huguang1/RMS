# -*- coding:utf-8 -*-
# author:无名
# datetime:2019/4/18 0018 12:56
# software: PyCharm
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
sex_dict = {"男": 1, "女": 2, "男女不限": 3}


class UrgencyJobDemandView(View):

    def get(self, request, pk=0):
        job_obj_list = models.Job.objects.all()
        hr_obj_list = models.User.objects.all()
        if not pk:
            try:
                current_page = int(request.GET.get("p"))
            except Exception as e:
                current_page = 1
            urgencyJobDemand_obj_list = models.UrgencyJobDemand.objects.all()
            posts = wu_paginator.WuPaginator(current_page, settings.MAX_PAGE_NUM, urgencyJobDemand_obj_list,
                                             settings.PER_PAGE).get_paginator()
            return render(request, "manage/ujdList.html",
                          {"posts":posts, "job_list": job_obj_list,
                           "hr_list": hr_obj_list})

        urgencyJobDemand_obj_list = models.UrgencyJobDemand.objects.filter(pk=pk)
        if not urgencyJobDemand_obj_list:
            return restful.params_error("你所选择的限时悬赏不存在")

        urgencyJobDemand = urgencyJobDemand_obj_list[0]

        return render(request, "manage/ujd.html",
                      {"ujd": urgencyJobDemand, "job_list": job_obj_list, "hr_list": hr_obj_list})

    def post(self, request, pk=0):
        form = forms.UrgencyJobDemandForm(request.POST)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())
        edu = form.cleaned_data.get("edu")
        work_time = form.cleaned_data.get("work_time")
        work_addr = form.cleaned_data.get("work_addr")
        status = form.cleaned_data.get("status")
        rebate = form.cleaned_data.get("rebate")
        salary = form.cleaned_data.get("salary")
        work = request.POST.get("work")
        need = request.POST.get("need")
        sex = request.POST.get("sex")
        essential_condition = request.POST.get("essential_condition")
        performance = request.POST.get("performance")
        note = request.POST.get("note")
        hr_id = request.POST.getlist("hr_id")[0]
        job_id = request.POST.getlist("job_id")[0]
        print(hr_id)
        sex = sex_dict.get(sex, None)
        if sex == None:
            return restful.params_error("请选择性别")
        if not hr_id.isdigit():
            return restful.params_error("请选择对接人")
        if not job_id.isdigit():
            return restful.params_error("请选择岗位")

        hr_id, job_id = int(hr_id), int(job_id)
        hr_obj_list = models.User.objects.filter(pk=hr_id)
        if not hr_obj_list:
            return restful.params_error("你所选择的对接人不存在")
        job_obj_list = models.Job.objects.filter(pk=job_id)
        if not job_obj_list:
            return restful.params_error("你所选择的岗位不存在")
        hr = hr_obj_list[0]
        job = job_obj_list[0]
        try:
            models.UrgencyJobDemand.objects.create(salary=salary, edu=edu, work=work, need=need, sex=sex,
                                                   status=status, rebate=rebate, hr=hr, job=job, note=note,
                                                   work_time=work_time, work_addr=work_addr, performance=performance,
                                                   essential_condition=essential_condition)
        except Exception as e:
            logger.error(e)
            return restful.server_error("限时悬赏创建失败,服务器异常")

        add_logs.add_log("创建限时悬赏", f"创建限时悬赏{job.name}", request.user)
        return restful.ok()

    def put(self, request, pk=0):
        urgencyJobDemand_obj_list = models.UrgencyJobDemand.objects.filter(pk=pk)
        if not urgencyJobDemand_obj_list:
            return restful.params_error("你所修改的岗位需求不存在")

        put = QueryDict(request.body)
        form = forms.UrgencyJobDemandForm(put)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())

        edu = form.cleaned_data.get("edu")
        work_time = form.cleaned_data.get("work_time")
        work_addr = form.cleaned_data.get("work_addr")
        status = form.cleaned_data.get("status")
        rebate = form.cleaned_data.get("rebate")
        salary = form.cleaned_data.get("salary")
        work = put.get("work")
        need = put.get("need")
        sex = put.get("sex")
        essential_condition = put.get("essential_condition")
        performance = put.get("performance")
        note = put.get("note")
        hr_id = put.getlist("hr_id")[0]
        job_id = put.getlist("job_id")[0]
        sex = sex_dict.get(sex, None)
        if sex == None:
            return restful.params_error("请选择性别")
        if not hr_id.isdigit():
            return restful.params_error("请选择对接人")
        if not job_id.isdigit():
            return restful.params_error("请选择岗位")

        hr_id, job_id = int(hr_id), int(job_id)
        hr_obj_list = models.User.objects.filter(pk=hr_id)
        if not hr_obj_list:
            return restful.params_error("你所选择的对接人不存在")
        job_obj_list = models.Job.objects.filter(pk=job_id)
        if not job_obj_list:
            return restful.params_error("你所选择的岗位不存在")
        hr = hr_obj_list[0]
        job = job_obj_list[0]

        try:
            urgencyJobDemand_obj_list.update(salary=salary, edu=edu, work=work, need=need, sex=sex,
                                                   status=status, rebate=rebate, hr=hr, job=job, note=note,
                                                   work_time=work_time, work_addr=work_addr, performance=performance,
                                                   essential_condition=essential_condition)
        except Exception as e:
            logger.error(e)
            return restful.server_error("限时悬赏修改失败,服务器异常")

        add_logs.add_log("修改限时悬赏", f"修改限时悬赏{job.name}", request.user)
        return restful.ok()

    def delete(self, request, pk=0):
        urgencyJobDemand_obj_list = models.UrgencyJobDemand.objects.filter(pk=pk)
        if not urgencyJobDemand_obj_list:
            return restful.params_error("你所删除的限时悬赏不存在")
        try:
            urgencyJobDemand = urgencyJobDemand_obj_list[0]
            urgencyJobDemand_obj_list.delete()
        except Exception as e:
            logger.error(e)
            return restful.server_error("限时悬赏删除失败,服务器异常")

        add_logs.add_log("删除限时悬赏", f"删除限时悬赏{urgencyJobDemand.job.name}", request.user)
        return restful.ok()
