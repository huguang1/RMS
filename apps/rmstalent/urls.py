from django.urls import path

from .views import UploadView
from .views import TalentView
from .views import TalentDetailView
from .views import TalentEntryInfoView
from .views import RegionView
from .views import InterviewedCompanyView
from .views import TalentListView

app_name = 'rms_talent'

urlpatterns = [
    path('upload/', UploadView.as_view(), name="upload"),
    path('', TalentView.as_view(), name="talent"),
    path('talentlist/', TalentListView.as_view(), name="talentlist"),
    path('detail/<int:data>/', TalentDetailView.as_view(), name="detail"),
    path('entryinfo/', TalentEntryInfoView.as_view(), name="entryinfo"),
    path('region/', RegionView.as_view(), name="region"),
    path('interviewed/', InterviewedCompanyView.as_view(), name="interviewed"),
]
