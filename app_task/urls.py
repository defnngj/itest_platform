from django.urls import path
from app_task import views

urlpatterns = [
    # 任务管理
    path('', views.task_manage),
    path('add/', views.add_task),
    path('edit/<int:tid>/', views.edit_task),
    path('delete/<int:tid>/', views.delete_task),
    path('result/<int:tid>/', views.task_result),

    # 接口
    path('case_node/', views.case_node),
    path('save_task/', views.save_task),
    path('run_task/', views.run_task),
    path('see_log/', views.see_log),
]
