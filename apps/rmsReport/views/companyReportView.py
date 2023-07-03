from django.shortcuts import render

# Create your views here
from apps.rmstalent.models import Talent
from apps.rmsauth.models import Group

from utils import restful, date_handle


def companyReportView(request):
    return render(request, "report/companyReport.html", date_handle.time_now)


def companyReportAjax(request):
    group_list = Group.objects.all()
    year, month = request.GET.get("year"), request.GET.get('month')
    try:
        int(year), int(month)
    except Exception as e:
        return restful.params_error("年月必须为整数")
    report, entry_sum, underway_sum, admit_sum = [], 0, 0, 0

    for group in group_list:
        company_list = [company for user in group.users.all() for company in user.companys.all()]
        group_entry_sum, group_underway_sum, group_admit_sum = 0, 0, 0

        for company in company_list:
            company_talent_list = Talent.objects.filter(admit_company=company)
            entry_count = len(company_talent_list.filter(entry_date__year=year, entry_date__month=month))
            admit_count = len(company_talent_list.filter(admit_date__year=year, admit_date__month=month))
            underway_count = len(company_talent_list.filter(underway=True))


            entry_sum += entry_count
            group_entry_sum += entry_count
            underway_sum += underway_count
            group_underway_sum += underway_count
            admit_sum += admit_count
            group_admit_sum += admit_count

            report.append({"company_code": company.code, "group_title": group.title, "entry_count": entry_count,
                           "underway_count": underway_count, "admit_count": admit_count})

        report.append({"company_code": "总计", "group_title": group.title, "entry_count": group_entry_sum,
                       "underway_count": group_underway_sum, "admit_count": group_admit_sum})

    report.append({"company_code": "总计", "group_title": "总计", "entry_count": entry_sum, "underway_count": underway_sum,
                   "admit_count": admit_sum})

    return restful.result(code=200, data=report)
