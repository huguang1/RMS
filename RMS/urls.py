"""RMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.urls import include
from utils.error import Error404

urlpatterns = [
    path('', include('apps.rmsindex.urls')),
    path('error404/', Error404.as_view(), name="error404"),
    path('account/', include('apps.rmsauth.urls', namespace="account")),
    path('syslogs/', include('apps.rmslogs.urls')),
    path('talent/', include('apps.rmstalent.urls')),
    path('manager/', include("apps.rmsManager.urls", namespace="manager")),
    path('talent/', include('apps.rmstalent.urls', namespace="talent")),
    path('report/', include("apps.rmsReport.urls", namespace="report")),
]
