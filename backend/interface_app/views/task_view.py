import os
from django.http import JsonResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.decorators import action
from common_app.utils import response, Error, response_fail
from interface_app.serializers import TaskSerializer, TaskValidators
from common_app.utils import Pagination

from backend import settings
from interface_app.models.project import Project
from interface_app.models.module import Module
from interface_app.models.case import TestCase
from interface_app.models.task import TestTask
from interface_app.models.task import TestResult
from interface_app.task_extend.task_thread import TaskThread

BASE_PATH = settings.BASE_DIR
EXTEND_DIR = os.path.join(BASE_PATH, "interface_app", "task_extend")


class TaskViewSet(ViewSet):
    queryset = TestTask.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = []

    @action(methods=["post"], detail=False, url_path='create')
    def create_task(self, request, *args, **kwargs):
        """
        创建任务
        """
        val = TaskValidators(data=request.data)
        if val.is_valid():
            val.save()
        else:
            return response_fail(val.errors)
        return response()

    @action(methods=["put"], detail=False, url_path='update')
    def update_task(self, request, *args, **kwargs):
        """
        创建任务
        """
        cid = request.data.get("id")
        if cid is None:
            return response(error=Error.CASE_ID_NULL)
        task = TestTask.objects.get(pk=cid, is_delete=False)
        val = TaskValidators(instance=task, data=request.data)
        if val.is_valid():
            val.save()
        else:
            return response_fail(val.errors)
        return response()

    @action(methods=["delete"], detail=True, url_path='delete')
    def delete_task(self, request, *args, **kwargs):
        """
        删除用例
        /api/interface/v1/task/<pk>/delete/
        """
        pk = kwargs.get("pk")
        if pk is None:
            return response(error=Error.CASE_ID_NULL)

        task = TestTask.objects.filter(id=pk, is_delete=False).update(is_delete=True)
        if task == 0:
            return response(error=Error.CASE_OBJECT_NULL)

        return response()

    @action(methods=["get"], detail=False, url_path='list')
    def get_task_list(self, request, *args, **kwargs):
        """
        获得用例数据
        /api/interface/v1/task/list/
        """
        test_case = TestTask.objects.filter(is_delete=False).all()
        pg = Pagination()
        page_module = pg.paginate_queryset(queryset=test_case, request=request, view=self)
        ser = TaskSerializer(instance=page_module, many=True)
        data = {
            "total": test_case.count(),
            "caseList": ser.data
        }
        return response(data=data)

    @action(methods=["get"], detail=True, url_path='info')
    def get_task(self, request, *args, **kwargs):
        """
        获得用例数据
        /api/interface/v1/task/<pk>/info/
        """
        pk = kwargs.get("pk")
        if pk is not None:
            try:
                task = TestTask.objects.get(id=pk, is_delete=False)
                ser = TaskSerializer(instance=task, many=False)
            except TestTask.DoesNotExist:
                return response(error=Error.CASE_ID_NULL)
            return response(data=ser.data)


def case_node(request):
    """
    获得用例树形结构
    """
    if request.method == "GET":
        projects = Project.objects.all()
        data_list = []
        for project in projects:
            project_dict = {
                "name": project.name,
                "isParent": True
            }

            modules = Module.objects.filter(project_id=project.id)
            module_list = []
            for module in modules:
                module_dict = {
                    "name": module.name,
                    "isParent": True
                }

                cases = TestCase.objects.filter(module_id=module.id)
                case_list = []
                for case in cases:
                    case_dict = {
                        "name": case.name,
                        "isParent": False,
                        "id": case.id,
                    }
                    case_list.append(case_dict)

                module_dict["children"] = case_list
                module_list.append(module_dict)

            project_dict["children"] = module_list
            data_list.append(project_dict)

        return JsonResponse({"status": 10200, "message": "success", "data": data_list})

    if request.method == "POST":
        tid = request.POST.get("tid", "")
        if tid == "":
            return JsonResponse({"status": 10200, "message": "任务id不能为空"})

        task = TestTask.objects.get(id=tid)
        case_list = task.cases[1:-1].split(",")
        case_list_int = []
        for case in case_list:
            case_list_int.append(int(case))

        task_data = {
            "taskName": task.name,
            "taskDesc": task.describe
        }

        projects = Project.objects.all()
        data_list = []
        for project in projects:
            project_dict = {
                "name": project.name,
                "isParent": True
            }

            modules = Module.objects.filter(project_id=project.id)
            module_list = []
            for module in modules:
                module_dict = {
                    "name": module.name,
                    "isParent": True
                }

                cases = TestCase.objects.filter(module_id=module.id)
                case_list = []
                for case in cases:
                    if case.id in case_list_int:
                        case_dict = {
                            "name": case.name,
                            "isParent": False,
                            "id": case.id,
                            "checked": True,
                        }
                    else:
                        case_dict = {
                            "name": case.name,
                            "isParent": False,
                            "id": case.id,
                            "checked": False,
                        }
                    case_list.append(case_dict)

                module_dict["children"] = case_list
                module_list.append(module_dict)

            project_dict["children"] = module_list
            data_list.append(project_dict)
        task_data["cases"] = data_list
        return JsonResponse({"status": 10200, "message": "success", "data": task_data})


def run_task(request):
    """ 运行任务 """
    if request.method == "POST":
        tid = request.POST.get("task_id", "")
        if tid == "":
            return JsonResponse({"status": 10200, "message": "task id is null"})

        # 1、在执行线程之前，判断当前有没有任务在执行？
        tasks = TestTask.objects.all()
        for t in tasks:
            if t.status == 1:
                return JsonResponse({"status": 10200, "message": "当前有任务正在执行！"})

        # 2. 修改任务的状态为：1-执行中
        task = TestTask.objects.get(id=tid)
        task.status = 1
        task.save()

        # 通过多线程运行测试任务
        TaskThread(tid).run()

        return JsonResponse({"status": 10200, "message": "任务开始执行！"})

    else:
        return JsonResponse({"status": 10101, "message": "请求方法错误"})


def see_log(request):
    """
    查看结果的日志
    """
    if request.method == "POST":
        rid = request.POST.get("result_id", "")
        if rid == "":
            return JsonResponse({"status": 10102, "message": "id不能为空"})
        r = TestResult.objects.get(id=rid)
        return JsonResponse({"status": 10200, "message": "", "data": r.result})
    else:
        return JsonResponse({"status": 10101, "message": "请求方法错误"})
