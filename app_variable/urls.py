from django.urls import path
from app_variable import views

urlpatterns = [
    # 任务管理
    path('', views.variable_manage),

]