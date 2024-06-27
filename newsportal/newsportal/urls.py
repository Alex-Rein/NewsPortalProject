"""
URL configuration for newsportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from news.views import Index

urlpatterns = [
    path('i18n', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
    path('', RedirectView.as_view(pattern_name='news_list'), name='index'),
    path('articles/', include('news.urls2')),
    path('accounts/', include('allauth.urls')),
    path('test/', Index.as_view())
]
