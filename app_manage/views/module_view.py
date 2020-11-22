from django.shortcuts import render
from django.http import HttpResponseRedirect
from app_manage.forms import ModuleForm
from app_manage.models.module import Module


def manage_module(request):
    """
    模块管理
    """
    module_list = Module.objects.all()
    return render(request, "module/list.html", {
        "modules": module_list})


def add_module(request):
    """创建模块"""
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            Module.objects.create(name=name, describe=describe, project=project)

        return HttpResponseRedirect("/manage/module_list/")
    else:
        form = ModuleForm()
    return render(request, 'module/add.html', {'form': form})


def edit_module(request, mid):
    """
    编辑项目
    :param request:
    :param mid:
    """
    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            project = form.cleaned_data['project']
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']

            m = Module.objects.get(id=mid)
            m.project = project
            m.name = name
            m.describe = describe
            m.save()
        return HttpResponseRedirect("/manage/module_list/")
    else:
        if mid:
            m = Module.objects.get(id=mid)
            form = ModuleForm(instance=m)
        else:
            form = ModuleForm()
        return render(request, 'module/edit.html', {
            'form': form, "id": mid})


def delete_module(request, mid):
    """
    删除模块
    :param request:
    :param mid:
    """
    if request.method == "GET":
        m = Module.objects.get(id=mid)
        m.delete()
        return HttpResponseRedirect("/manage/module_list/")
    else:
        return HttpResponseRedirect("/manage/module_list/")
