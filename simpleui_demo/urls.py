# """simpleui_demo URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/2.1/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.conf import settings
# from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls. static import static


from ptclass.admin import show_medical_report
from ptclass.views import export_report
from simpleui_demo.settings import MEDIA_ROOT

admin.site.site_title = '管道辅助系统'
admin.site.site_header = '智慧管网'

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('ptclass/medical-report/', show_medical_report, name='ptclass_medical_report'),
                  # 配置admindoc
                  path(r'doc/', include('django.contrib.admindocs.urls'), name='doc'),
                  path('', admin.site.urls),
                  path(r'mdeditor/', include('mdeditor.urls')),
                  path('ptclass/', include('ptclass.urls')),  # 确保包含 ptclass 的 URL 配置
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""simpleui_demo URL Configuration

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
# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.contrib.staticfiles.views import serve
# from django.urls import path, include
#
# from ptclass.admin import show_medical_report
# from ptclass.views import export_report
# from simpleui_demo.settings import MEDIA_ROOT
#
# admin.site.site_title = '管道辅助系统'
# admin.site.site_header = '智慧管网'
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('/', admin.site.urls),
#     path('ptclass/medical-report/', show_medical_report, name='ptclass_medical_report'),
#     # 配置admindoc
#     path('doc/', include('django.contrib.admindocs.urls'), name='doc'),
#     path('mdeditor/', include('mdeditor.urls')),
#     path('ptclass/', include('ptclass.urls')),  # 确保包含 ptclass 的 URL 配置
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

