import json
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itest_platform import settings
from app_manage.models import Project
from app_manage.models import Module
from app_case.models import TestCase
from app_task.models import TestTask
from app_task.models import TestResult
from app_task.extend.task_thread import TaskThread

BASE_PATH = settings.BASE_DIR.replace("\\", "/")
EXTEND_DIR = BASE_PATH + "/testtask_app/extend/"


def task_manage(request):
    """
    任务管理
    """
    task_list = TestTask.objects.all()
    return render(request, "task/list.html", {"tasks": task_list})


def add_task(request):
    """
    返回创建任务页面
    """
    return render(request, "task/add.html")


def edit_task(request, tid):
    """
    返回编辑任务页面
    """
    return render(request, "task/edit.html")


def task_result(request, tid):
    """
    任务执行结果
    """
    results = TestResult.objects.filter(task_id=tid).order_by('-create_time')
    p = Paginator(results, 5)
    page = request.GET.get("page", "")
    if page == "":
        page = 1

    try:
        page_result = p.page(page)
    except EmptyPage:
        page_result = p.page(p.num_pages)
    except PageNotAnInteger:
        page_result = p.page(1)
    return render(request, "task/result.html", {"results": page_result})


def delete_task(request, tid):
    """
    删除任务
    """
    task = TestTask.objects.get(id=tid)
    task.delete()
    return HttpResponseRedirect("/task/")


def save_task(request):
    """
    创建/保存任务
    """
    if request.method == "POST":
        task_id = request.POST.get("task_id", "")
        name = request.POST.get("name", "")
        desc = request.POST.get("desc", "")
        cases = request.POST.get("cases", "")

        if name == "" or cases == "":
            return JsonResponse({"status": 10102, "message": "Parameter is null"})

        if task_id == "0":
            TestTask.objects.create(name=name, describe=desc, cases=cases)
        else:
            task = TestTask.objects.get(id=task_id)
            task.name = name
            task.describe = desc
            task.cases = cases
            task.save()

        return JsonResponse({"status": 10200, "message": "success"})
    else:
        return JsonResponse({"status": 10101, "message": "请求方法错误"})


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
