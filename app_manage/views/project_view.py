from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app_manage.models.project import Project
from app_manage.forms import ProjectForm, ProjectEditForm


@login_required
def mange_project(request):
    """
    项目管理
    """
    project_list = Project.objects.all()
    username = request.session.get('user', 'guest')
    return render(request, "project/list.html", {"projects": project_list, "user": username})


def add_project(request):
    """
    创建项目
    """
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']
            Project.objects.create(name=name, describe=describe, status=status)

        return HttpResponseRedirect("/manage/")
    else:
        form = ProjectForm()
    return render(request, 'project/add.html', {'form': form})


def edit_project(request, pid):
    """
    编辑项目
    """
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']

            p = Project.objects.get(id=pid)
            p.name = name
            p.describe = describe
            p.status = status
            p.save()
        return HttpResponseRedirect("/manage/")
    else:
        if pid:
            p = Project.objects.get(id=pid)
            form = ProjectEditForm(instance=p)
        else:
            form = ProjectForm()
        return render(request, 'project/edit.html', {
            'form': form, "id": pid})


def delete_project(request, pid):
    """
    删除项目
    :param request:
    :param pid:
    """
    if request.method == "GET":
        p = Project.objects.get(id=pid)
        p.delete()
        return HttpResponseRedirect("/manage/")
    else:
        return HttpResponseRedirect("/manage/")
