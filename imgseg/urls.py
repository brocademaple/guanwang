from django.urls import path
from imgseg import views

app_name = 'imgseg'  # 定义命名空间

urlpatterns = [
    path('image/', views.ImageView.as_view(), name='image'),  # 确保这个名称与 reverse() 中的一致
]