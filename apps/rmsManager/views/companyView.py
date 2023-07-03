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


# 每页显示的数据条数


class CompanyView(View):

    def get(self, request, pk=0):
        """
        每页显示10条数据
        :param request:
        :param pk:
        :return:
        """
        hr_obj_list = User.objects.all()
        if not pk:
            try:
                current_page = int(request.GET.get("p"))
            except Exception as e:
                current_page = 1
            company_obj_list = models.Company.objects.all().order_by("id")
            posts = wu_paginator.WuPaginator(current_page, settings.MAX_PAGE_NUM, company_obj_list,
                                             settings.PER_PAGE).get_paginator()
            return render(request, "manage/companyList.html", {"hr_list": hr_obj_list, "posts": posts})

        company_obj_list = models.Company.objects.filter(pk=pk)
        if not company_obj_list:
            return restful.params_error("你所选择的公司不存在")

        company = company_obj_list[0]
        # my_hr = company.hr
        return render(request, "manage/company.html",
                      {"company": company, "hr_list": hr_obj_list})

    def post(self, request, pk=0):
        form = forms.CompanyFrom(request.POST)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())

        code = form.cleaned_data.get("code")
        cooperation_models = form.cleaned_data.get("cooperation_models")
        area = form.cleaned_data.get("area")
        block = form.cleaned_data.get("block")
        floor = form.cleaned_data.get("floor")
        addr = form.cleaned_data.get("addr")
        rebate = request.POST.get("rebate")
        hr_id = request.POST.getlist("hr_id")[0]

        if models.Company.objects.filter(code=code):
            return restful.params_error("你所添加的公司代码已经存在")
        if not hr_id.isdigit():
            return restful.params_error("请选择对接人")

        hr_id = int(hr_id)
        hr_obj_list = User.objects.filter(pk=hr_id)
        if not hr_obj_list:
            return restful.params_error("你所选择的对接人不存在")
        hr = hr_obj_list[0]
        if hr.is_superuser:
            return restful.params_error("不能选择非招聘组成员为对接人")
        try:
            models.Company.objects.create(code=code, cooperation_models=cooperation_models, area=area,
                                          block=block, floor=floor, addr=addr, rebate=rebate, hr=hr)
        except Exception as e:
            logger.error(e)
            return restful.server_error("公司创建失败,服务器异常")

        add_logs.add_log("创建公司", f"创建公司{code}", request.user)
        return restful.ok()

    def put(self, request, pk=0):
        company_obj_list = models.Company.objects.filter(pk=pk)
        if not company_obj_list:
            return restful.params_error("你所修改的公司不存在")

        put = QueryDict(request.body)
        form = forms.CompanyFrom(put)
        if not form.is_valid():
            return restful.params_error(message=form.get_errors())

        code = form.cleaned_data.get("code")
        cooperation_models = form.cleaned_data.get("cooperation_models")
        area = form.cleaned_data.get("area")
        block = form.cleaned_data.get("block")
        floor = form.cleaned_data.get("floor")
        addr = form.cleaned_data.get("addr")
        rebate = put.get("rebate")
        hr_id = put.getlist("hr_id")[0]

        if code != company_obj_list[0].code and models.Company.objects.filter(code=code):
            return restful.params_error("已经有相同代码的公司存在,请换个代码")

        if not hr_id.isdigit():
            return restful.params_error("请选择对接人")

        hr_id = int(hr_id)
        hr_obj_list = User.objects.filter(pk=hr_id)
        if not hr_obj_list:
            return restful.params_error("你所选择的对接人不存在")
        hr = hr_obj_list[0]
        if hr.is_superuser:
            return restful.params_error("不能选择非招聘组成员为对接人")
        try:
            company_obj_list.update(code=code, cooperation_models=cooperation_models, area=area,
                                    block=block, floor=floor, addr=addr, rebate=rebate, hr=hr)
        except Exception as e:
            logger.error(e)
            return restful.server_error("公司信息修改失败,服务器异常")

        add_logs.add_log("编辑公司", f"编辑公司{code}", request.user)
        return restful.ok()

    def delete(self, request, pk=0):
        company_obj_list = models.Company.objects.filter(pk=pk)
        if not company_obj_list:
            return restful.params_error("你所删除的公司不存在")
        try:
            code = company_obj_list[0].code
            company_obj_list.delete()
        except Exception as e:
            logger.error(e)
            return restful.server_error("公司信息删除失败,服务器异常")

        add_logs.add_log("删除公司", f"删除公司{code}", request.user)
        return restful.ok()
