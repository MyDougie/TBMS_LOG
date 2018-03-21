"""TbmsLog URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from TbmsLog.views import HomeView
from TbmsLog.views import ReadFileView, ReadFileResultView, LogResultView
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^read_file_view/$' , ReadFileView.as_view(), name='read_file_view'),
    #url(r'^read_file/$', ReadFileResultView.as_view(), name='read_file_result_view'),
    #url(r'^(?P<path>\d+)/$', views.test, name='read_file'),
    url(r'^read_file/$', views.read_file, name='read_file'),
    url(r'^log_result/$' , LogResultView.as_view(), name='log_result_view'),
]
