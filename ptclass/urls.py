# ptclass/urls.py
from django.urls import path
from .views import export_report

urlpatterns = [
    path('export-report/', export_report, name='export_report'),  # 此处定义的路径
    # 其他 URL 路由...
]