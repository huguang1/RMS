from django.urls import path

from .views import LogsView


app_name = 'rms_syslogs'

urlpatterns = [
    path('', LogsView.as_view(), name='syslogs')
]
