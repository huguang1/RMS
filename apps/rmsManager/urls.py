from django.urls import path

from apps.rmsManager.views import companyView, urgencyJobDemandView, recruitmentWayView, jobView, jobDemandView

app_name = 'rmsCompany'

urlpatterns = [
    path('job/<int:pk>/', jobView.JobView.as_view(), name="job"),
    path('job/', jobView.JobView.as_view(), name="job"),

    path('recruitment_way/<int:pk>/', recruitmentWayView.RecruitmentWayView.as_view(), name="recruitmentWay"),
    path('recruitment_way/', recruitmentWayView.RecruitmentWayView.as_view(), name="recruitmentWay"),

    path('company/<int:pk>/', companyView.CompanyView.as_view(), name="company"),
    path('company/', companyView.CompanyView.as_view(), name="company"),

    path('job_demand/<int:pk>/', jobDemandView.JobDemandView.as_view(), name="jobDemand"),
    path('job_demand/', jobDemandView.JobDemandView.as_view(), name="jobDemand"),

    path('foreign_job_demand/<int:pk>/', jobDemandView.JobDemandView.as_view(), {"job_type": 2},
         name="foreignJobDemand"),
    path('foreign_job_demand/', jobDemandView.JobDemandView.as_view(), {"job_type": 2}, name="foreignJobDemand"),

    path('urgency_job_demand/<int:pk>/', urgencyJobDemandView.UrgencyJobDemandView.as_view(), name="urgencyJobDemand"),
    path('urgency_job_demand/', urgencyJobDemandView.UrgencyJobDemandView.as_view(), name="urgencyJobDemand"),
]
