# -*- coding:utf-8 -*-
# author:无名
# datetime:2019/5/9 0009 14:39
# software: PyCharm
import datetime
from django.shortcuts import render

from apps.rmstalent.models import Talent, Status
from apps.rmsauth.models import Group
from apps.rmsManager.models import Company

from utils import restful, date_handle


def admitReportView(request):
    return render(request, "report/admitReport.html", date_handle.time_now)


def admitReportAjax(request):
    start_time = request.GET.get("start")+" 00:00:00"
    end_time = request.GET.get("end")+" 23:59:59"
    try:
        start_time = date_handle.str_to_datetime(start_time)
        end_time = date_handle.str_to_datetime(end_time)
    except Exception:
        return restful.params_error("时间格式不正确, 应该是YYYY-MM-DD")

    company_list = Company.objects.all()
    group_list = Group.objects.all()
    talent_list = Talent.objects.filter(admit_date__range=(start_time,end_time))
    # report:主要数据 company_code_list :前端展示数据表单横向公司代码数据
    report = []
    c_i = 0  # company循环次数,从0开始计数

    company_code_list = [company.code for company in company_list]
    for company in company_list:
        c_i += 1
        r_i = -1  # report的索引,从-1开始计数
        talent_company_list = talent_list.filter(admit_company_id=company.id)
        for group in group_list:
            r_i += 1
            g_i = r_i  # 当前group 在report的索引
            if c_i == 1:
                report.append({"group_user": group.title,"type":"group"})
            group_sum = 0
            for user in group.users.all():
                r_i += 1
                if c_i == 1:
                    report.append({"group_user": user.username,"type":"user"})
                user_count = len(talent_company_list.filter(user_id=user.id))
                group_sum += user_count
                report[r_i].setdefault(company.code, user_count)

            report[g_i].setdefault(company.code, group_sum)
    return restful.result(code=200, data={"report": report, "company": company_code_list})


def leaveReportAjax(request):
    start_time = request.GET.get("start") + " 00:00:00"
    end_time = request.GET.get("end") + " 23:59:59"
    try:
        start_time = date_handle.str_to_datetime(start_time)
        end_time = date_handle.str_to_datetime(end_time)
    except Exception:
        return restful.params_error("时间格式不正确, 应该是YYYY-MM-DD")

    report = []
    for company in Company.objects.all():
        entry_count = len(Talent.objects.filter(entry_date__range=(start_time,end_time)))
        leave_count = len(Status.objects.filter(code=7,time__range=(start_time,end_time)))
        report.append({"company":company.code,"entry_count":entry_count,"leave_count":leave_count,"percent": '{:.2%}'.format(leave_count / entry_count if entry_count else leave_count)})
    return restful.result(code=200,data=report)