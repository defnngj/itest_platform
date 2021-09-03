from django.urls import path
from rest_framework import routers
from interface_app.views.project_view import ProjectView
from interface_app.views.module_view import ModuleView, ModuleTreeView
from interface_app.views.case_view import CaseView, CaseViewSet
from interface_app.views.task_view import TaskViewSet

urlpatterns = [
    # 项目管理
    path('v1/project/<int:pk>/', ProjectView.as_view()),
    path('v1/project/', ProjectView.as_view()),

    # 模块管理
    path('v1/module/<int:pk>/', ModuleView.as_view()),
    path('v1/module/', ModuleView.as_view()),
    path('v1/module/tree', ModuleTreeView.as_view()),

    # 用例管理
    # path('v1/case/', CaseView.as_view()),
    # path('v1/case/<int:pk>/', CaseView.as_view()),
]

router = routers.SimpleRouter()
router.register(r'v1/case', CaseViewSet)  # 用例管理
router.register(r'v1/task', TaskViewSet)  # 任务管理

urlpatterns += router.urls
