import logging
from django.shortcuts import render
from django.views import View
from django.http import QueryDict
from django.conf import settings

from utils import restful, add_logs, wu_paginator

from apps.rmsManager import forms
from apps.rmsManager import models

logger = logging.getLogger("django")
sex_dict = {"男": 1, "女": 2, "男女不限": 3}


class JobDemandView(View):

    def get(self, request, pk=0, job_type=1):
        job_obj_list = models.Job.objects.all()
        company_obj_list = models.Company.objects.all()
        if not pk:
            try:
                current_page = int(request.GET.get("p"))
            except Exception as e:
                current_page = 1
            jobDemand_obj_list = models.JobDemand.objects.filter(job_type=job_type).order_by("id")
            posts = wu_paginator.WuPaginator(current_page, settings.MAX_PAGE_NUM, jobDemand_obj_list,
                                             settings.PER_PAGE).get_paginator()
            return render(request, "manage/jobDemandList.html",
                          {"posts": posts, "job_type": job_type, "job_list": job_obj_list,
                           "company_list": company_obj_list})

        jobDemand_obj_list = models.JobDemand.objects.filter(pk=pk, job_type=job_type)
        if not jobDemand_obj_list:
            return restful.params_error("你所选择的岗位需求不存在")

        jobDemand = jobDemand_obj_list[0]

        return render(request, "manage/jobDemand.html",
                      {"jobDemand": jobDemand, "job_list": job_obj_list, "company_list": company_obj_list,
                       "job_type": job_type})

    def post(self, request, pk=0, job_type=1):
        form = forms.JobDemandForm(request.POST)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())
        probation_salary = form.cleaned_data.get("probation_salary")
        salary = form.cleaned_data.get("salary")
        work_time = form.cleaned_data.get("work_time")
        holiday = form.cleaned_data.get("holiday")
        nums = form.cleaned_data.get("nums")
        edu = form.cleaned_data.get("edu")
        work_years = form.cleaned_data.get("work_years")
        dorm = form.cleaned_data.get("dorm")
        recruitment_way = form.cleaned_data.get("recruitment_way")
        work = request.POST.get("work")
        need = request.POST.get("need")
        sex = request.POST.get("sex")
        essential_condition = request.POST.get("essential_condition")
        salary_method = request.POST.get("salary_method")
        performance = request.POST.get("performance")
        job_subsidy = request.POST.get("job_subsidy")
        life_subsidy = request.POST.get("life_subsidy")
        welfare = request.POST.get("welfare")
        note = request.POST.get("note")
        company_id = request.POST.getlist("company_id")[0]
        job_id = request.POST.getlist("job_id")[0]
        sex = sex_dict.get(sex, None)
        if sex == None:
            return restful.params_error("请选择性别")
        if not company_id.isdigit():
            return restful.params_error("请选择公司")
        if not job_id.isdigit():
            return restful.params_error("请选择岗位")

        company_id, job_id = int(company_id), int(job_id)
        company_obj_list = models.Company.objects.filter(pk=company_id)
        if not company_obj_list:
            return restful.params_error("你所选择的公司不存在")
        job_obj_list = models.Job.objects.filter(pk=job_id)
        if not job_obj_list:
            return restful.params_error("你所选择的岗位不存在")
        company = company_obj_list[0]
        job = job_obj_list[0]
        try:
            models.JobDemand.objects.create(probation_salary=probation_salary, salary=salary, work_time=work_time,
                                            holiday=holiday, nums=nums, edu=edu, work_years=work_years,
                                            recruitment_way=recruitment_way, dorm=dorm, work=work, need=need, sex=sex,
                                            essential_condition=essential_condition, salary_method=salary_method,
                                            performance=performance, job_subsidy=job_subsidy, life_subsidy=life_subsidy,
                                            welfare=welfare, note=note, company=company, job=job, job_type=job_type)
        except Exception as e:
            logger.error(e)
            return restful.server_error("岗位需求创建失败,服务器异常")

        add_logs.add_log("创建岗位需求", f"创建岗位需求{company.code}{job.name}", request.user)
        return restful.ok()

    def put(self, request, pk=0, job_type=1):
        jobDemand_obj_list = models.JobDemand.objects.filter(pk=pk, job_type=job_type)
        if not jobDemand_obj_list:
            return restful.params_error("你所修改的岗位需求不存在")

        put = QueryDict(request.body)
        form = forms.CompanyFrom(put)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())

        probation_salary = form.cleaned_data.get("probation_salary")
        salary = form.cleaned_data.get("salary")
        work_time = form.cleaned_data.get("work_time")
        holiday = form.cleaned_data.get("holiday")
        nums = form.cleaned_data.get("nums")
        edu = form.cleaned_data.get("edu")
        work_years = form.cleaned_data.get("work_years")
        recruitment_way = form.cleaned_data.get("recruitment_way")
        dorm = form.cleaned_data.get("dorm")
        work = put.get(" work")
        need = put.get(" need")
        sex = put.get("sex")
        essential_condition = put.get("essential_condition")
        salary_method = put.get("salary_method")
        performance = put.get("performance")
        job_subsidy = put.get("job_subsidy")
        life_subsidy = put.get("life_subsidy")
        welfare = put.get("welfare")
        note = put.get("note")
        company_id = put.getlist("company")[0]
        job_id = put.getlist("job")[0]
        sex = sex_dict.get(sex, None)
        if sex == None:
            return restful.params_error("请选择性别")
        if not company_id.isdigit():
            return restful.params_error("请选择公司")
        if not job_id.isdigit():
            return restful.params_error("请选择岗位")

        company_id, job_id = int(company_id), int(job_id)
        company_obj_list = models.Company.objects.filter(pk=company_id)
        if not company_obj_list:
            return restful.params_error("你所选择的公司不存在")
        job_obj_list = models.Job.objects.filter(pk=job_id)
        if not job_obj_list:
            return restful.params_error("你所选择的岗位不存在")
        company = company_obj_list[0]
        job = job_obj_list[0]

        try:
            jobDemand_obj_list.update(probation_salary=probation_salary, salary=salary, work_time=work_time,
                                      holiday=holiday, nums=nums, edu=edu, work_years=work_years,
                                      recruitment_way=recruitment_way, dorm=dorm, work=work, need=need, sex=sex,
                                      essential_condition=essential_condition, salary_method=salary_method,
                                      performance=performance, job_subsidy=job_subsidy, life_subsidy=life_subsidy,
                                      welfare=welfare, note=note, company=company, job=job, job_type=job_type)
        except Exception as e:
            logger.error(e)
            return restful.server_error("岗位需求修改失败,服务器异常")

        add_logs.add_log("修改岗位需求", f"修改岗位需求{company.name}{job.name}", request.user)
        return restful.ok()

    def delete(self, request, pk=0, job_type=1):
        jobDemand_obj_list = models.JobDemand.objects.filter(pk=pk, job_type=job_type)
        if not jobDemand_obj_list:
            return restful.params_error("你所删除的岗位需求不存在")
        try:
            jobDemand = jobDemand_obj_list[0]
            jobDemand_obj_list.delete()
        except Exception as e:
            logger.error(e)
            return restful.server_error("岗位需求删除失败,服务器异常")
        add_logs.add_log("删除岗位需求", f"删除岗位需求{jobDemand.company.code}{jobDemand.job.name}", request.user)
        return restful.ok()
