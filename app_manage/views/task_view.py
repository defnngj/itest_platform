from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_manage.models.task import TestTask
from app_manage.models.task import TestResult


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
    return HttpResponseRedirect("/manage/task/")
