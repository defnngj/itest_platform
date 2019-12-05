from django.urls import path
from app_task import views

urlpatterns = [
    # 任务管理
    path('', views.testtask_manage),
    path('add_task/', views.add_task),
    path('edit_task/<int:tid>/', views.edit_task),
    path('delete_task/<int:tid>/', views.delete_task),
    path('result/<int:tid>/', views.result),
    path('save_task/', views.save_task),

    # 接口
    path('get_case_tree/', views.get_case_tree),
    path('run_task/', views.run_task),
    path('see_log/', views.see_log),
]
