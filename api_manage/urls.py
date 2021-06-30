from django.urls import path
from api_manage.apis import case_api
from api_manage.apis import task_api
from api_manage.apis import variable_api


urlpatterns = [
    # 用例管理接口
    path('case_delete/', case_api.delete_case),
    path('send_req/', case_api.send_req),
    path('assert_result/', case_api.assert_result),
    path('get_select_data/', case_api.get_select_data),
    path('save_case/', case_api.save_case),
    path('get_case_info/', case_api.get_case_info),

    # 任务管理接口
    path('case_node/', task_api.case_node),
    path('save_task/', task_api.save_task),
    path('run_task/', task_api.run_task),
    path('see_log/', task_api.see_log),

    # 变量管理接口
    path('add_variable/', variable_api.add_variable),
    path('delete_variable/', variable_api.delete_variable),
]

