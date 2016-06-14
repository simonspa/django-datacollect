"""datacollect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
from survey.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^analysis/$', RecordAnalysis.as_view(), name='record_analysis'),

    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^map/$', RecordsMap.as_view(), name='map'),
    url(r'^map2/$', RecordsMap2.as_view(), name='map2'),
    url(r'^api/records.json$', cases_json, name='records-json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
