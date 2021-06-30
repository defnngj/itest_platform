from django.urls import path
from app_manage.views import project_view
from app_manage.views import module_view
from app_manage.views import case_view
from app_manage.views import task_view
from app_manage.views import variable_view

urlpatterns = [

    # 项目管理
    path('', project_view.mange_project),
    path('project/', project_view.mange_project),
    path('project_add/', project_view.add_project),
    path('project_edit/<int:pid>/', project_view.edit_project),
    path('project_delete/<int:pid>/', project_view.delete_project),

    # 模块管理
    path('module/', module_view.manage_module),
    path('module_add/', module_view.add_module),
    path('module_edit/<int:mid>/', module_view.edit_module),
    path('module_delete/<int:mid>/', module_view.delete_module),

    # 用例管理
    path('case/', case_view.list_case),
    path('case_add/', case_view.add_case),
    path('case_edit/<int:cid>/', case_view.edit_case),

    # 任务管理
    path('task/', task_view.task_manage),
    path('task_add/', task_view.add_task),
    path('task_edit/<int:tid>/', task_view.edit_task),
    path('task_delete/<int:tid>/', task_view.delete_task),
    path('task_result/<int:tid>/', task_view.task_result),

    # 变量管理
    path('variable/', variable_view.variable_manage),
]

