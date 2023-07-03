from django.urls import path

from apps.rmsReport.views import companyReportView, groupReportView, admitReportView, targetReportView

app_name = 'rms_report'

urlpatterns = [
    path('company/ajax/', companyReportView.companyReportAjax, name='companyReportAjax'),
    path('company/', companyReportView.companyReportView, name='companyReport'),

    path('group/ajax/', groupReportView.groupReportAjax, name='groupReportAjax'),
    path('group/', groupReportView.groupReportView, name='groupReport'),

    path('leave/ajax/', admitReportView.leaveReportAjax, name='leaveReportAjax'),
    path('admit/ajax/', admitReportView.admitReportAjax, name='admitReportAjax'),
    path('admit/', admitReportView.admitReportView, name='admitReport'),

    path('target/ajax/', targetReportView.targetReportAjax, name='targetReportAjax'),
    path('target/view/', targetReportView.targetReportView, name='targetReport'),
    path('target/',targetReportView.TargetView.as_view(), name='target'),
]
