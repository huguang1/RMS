# -*- coding:utf-8 -*-
# author:无名
# datetime:2019/5/7 0007 15:54
# software: PyCharm
from django.shortcuts import render

from apps.rmstalent.models import Talent, Interview, Status
from apps.rmsauth.models import Group

from utils import restful, date_handle


def groupReportView(request):
    return render(request, "report/groupReport.html", date_handle.time_now)


def groupReportAjax(request):
    type = request.GET.get("type")
    report = []
    if type == "year":
        year = request.GET.get("year")
        try:
            int(year)
        except Exception as e:
            return restful.params_error("年份必须为整数")
        month = date_handle.year_month(int(year))

        interview_list = Interview.objects.filter(date__year=year)
        for now_month in range(1, month + 1):
            first_count = len(interview_list.filter(number=1, date__month=str(now_month)))
            last_count = len(interview_list.filter(number=2, date__month=str(now_month)))
            entry_count = len(Talent.objects.filter(entry_date__year=year, entry_date__month=str(now_month)))
            report.append({"month": f'{now_month}月', "first_count": first_count, "last_count": last_count,
                           "entry_count": entry_count})
    elif type == 'month':
        year, month = request.GET.get("year"), request.GET.get('month')
        try:
            int(year), int(month)
        except Exception as e:
            return restful.params_error("年月必须为整数")
        group_list = Group.objects.all()
        interview_list = Interview.objects.filter(date__year=year, date__month=month)
        entry_talent_list = Talent.objects.filter(entry_date__year=year, entry_date__month=month)
        fail_talent_list = [status.talent for status in
                            Status.objects.filter(time__year=year, time__month=month, code=6)]
        first_sum, last_sum, entry_sum, fail_sum = 0, 0, 0, 0

        for group in group_list:
            first_count = len(
                [interview for interview in interview_list.filter(number=1) if interview.talent.group_id == group.id])
            last_count = len(
                [interview for interview in interview_list.filter(number=2) if interview.talent.group_id == group.id])
            entry_count = len([talent for talent in entry_talent_list if talent.group_id == group.id])
            fail_count = len([talent for talent in fail_talent_list if talent.group_id == group.id])
            first_sum += first_count
            last_sum += last_count
            entry_sum += entry_count
            fail_sum += fail_count
            report.append(
                {"group": group.title, "first_count": first_count, "last_count": last_count, "entry_count": entry_count,
                 "fail_count": fail_count,
                 "percent": '{:.2%}'.format(fail_count / entry_count if entry_count else fail_count)})
        report.append({
            "group": "合计", "first_count": first_sum, "last_count": last_sum, "entry_count": entry_sum,
            "fail_count": fail_sum,
            "percent": '{:.2%}'.format(fail_sum / entry_sum if entry_sum else fail_sum)
        })
    else:
        return restful.params_error(message="type类型不对")
    return restful.result(code=200, data=report)
