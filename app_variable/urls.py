from django.urls import path
from app_variable import views

urlpatterns = [
    # 任务管理
    path('', views.variable_manage),
    path('add_variable/', views.add_variable),
    path('delete_variable/', views.delete_variable),

]