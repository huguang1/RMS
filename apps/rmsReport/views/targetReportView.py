# -*- coding:utf-8 -*-
# author:无名
# datetime:2019/5/12 0012 13:21
# software: PyCharm
from django.shortcuts import render, HttpResponse
from django.views import View

from utils import restful, date_handle, add_logs

from rmsReport.models import Target
from rmsReport.forms import TargetForm
from apps.rmsauth.models import Group
from apps.rmstalent.models import Talent

group_list = Group.objects.all()


def targetReportView(request):
    data = {"group_list":group_list}
    data.update(date_handle.time_now)
    return render(request, "report/targetReport.html",data)


def targetReportAjax(request):
    report = []
    year = request.GET.get("year")
    group_id = request.GET.get("group_id")
    if not group_id:
        return restful.params_error("你未选择,请选择一个小组进行查看")
    if not Group.objects.filter(id=int(group_id)):
        return restful.params_error("你选择的小组不存在")
    group = Group.objects.filter(id=int(group_id))[0]
    if int(year) == date_handle.time_now.get("year"):
        month = date_handle.time_now.get("month")
    else:
        month = 12

    group_count_dict = {"type": "当月组员人数"}
    resume_count_dict = {"type": "新增简历数(目标)"}
    admit_target_dict = {"type": "录取数(目标)"}
    admit_count_dict = {"type": "录取数(实际)"}
    entry_count_dict = {"type": "月报道人数(实际)"}
    target_avg_dict = {"type": "人均录取数(目标)"}
    admit_avg_dict = {"type": "人均录取数(实际)"}
    target_percent_dict = {"type": "报到成功率(目标)"}
    entry_percent_dict = {"type": "报到成功率(实际)"}
    month_list = list(range(1,month+1))
    target_list = Target.objects.filter(date__year=year,group_id=group.id)
    for i in range(1, month + 1):
        target = target_list.filter(date__month=i)
        admit_count = len(Talent.objects.filter(admit_date__year=year, admit_date__month=month,user__group__id=group.id))
        entry_count = len(Talent.objects.filter(entry_date__year=year, entry_date__month=month,user__group__id=group.id))
        admit_count_dict.update({i: admit_count})
        entry_count_dict.update({i: entry_count})
        entry_percent_dict.update({i: '{:.2%}'.format(entry_count / admit_count if admit_count else entry_count)})
        if not target:
            d = {i: "未设定目标"}
            group_count_dict.update(d)
            resume_count_dict.update(d)
            admit_target_dict.update(d)
            target_avg_dict.update(d)
            target_percent_dict.update(d)
            admit_avg_dict.update(d)
        else:
            target = target[0]
            group_count_dict.update({i: target.group_count})
            resume_count_dict.update({i: target.new_resume})
            admit_target_dict.update({i: target.admit_count})
            target_avg_dict.update({i: '%.2f' % (target.admit_count / target.group_count)})
            target_percent_dict.update({i: target.entry_percent})
            admit_avg_dict.update({i: '%.2f' % (admit_count / target.group_count)})
    report = [group_count_dict, resume_count_dict, admit_target_dict, admit_count_dict,
              entry_count_dict, target_avg_dict, admit_avg_dict, target_percent_dict, entry_percent_dict]
    return restful.result(code=200, data={"report":report,"month_list":month_list})


class TargetView(View):
    def get(self, request):
        group = request.user.group
        if not group:
            return HttpResponse("你不属于任何招聘组,没有权限编辑目标")
        year = date_handle.time_tomorrow.get("year")
        month = date_handle.time_tomorrow.get("month")
        print(year, month)
        target_list = Target.objects.filter(group=group,
                                            date__year=str(year),
                                            date__month=str(month))

        target = target_list[0] if target_list else {}
        data = date_handle.time_tomorrow
        data.setdefault("target", target)
        return render(request, "report/target.html", data)

    def post(self, request):
        group = request.user.group
        if not group:
            return restful.params_error("你不属于任何组")
        form = TargetForm(request.POST)
        if not form.is_valid():
            return restful.params_error(form.get_errors())
        group_count = form.cleaned_data.get("group_count")
        new_resume = form.cleaned_data.get("new_resume")
        admit_count = form.cleaned_data.get("admit_count")
        entry_count = form.cleaned_data.get("entry_count")
        entry_percent = '{:.2%}'.format(entry_count / admit_count if admit_count else entry_count)
        year = date_handle.time_tomorrow.get("year")
        month = date_handle.time_tomorrow.get("month")
        target_list = Target.objects.filter(group_id=group.id,
                                            date__year=str(year),
                                            date__month=str(month))
        try:
            if target_list:
                target_list.update(group_count=group_count, new_resume=new_resume, admit_count=admit_count,
                                   entry_count=entry_count, entry_percent=entry_percent)
            else:
                Target.objects.create(group=group, date=date_handle.tomorrow,
                                      group_count=group_count, new_resume=new_resume, admit_count=admit_count,
                                      entry_count=entry_count, entry_percent=entry_percent)
        except Exception as e:
            return restful.server_error("信息编辑失败")
        add_logs.add_log("编辑目标", f"编辑{group.title}目标", request.user)
        return restful.ok()
