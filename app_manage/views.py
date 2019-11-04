from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app_manage.models import Project
from app_manage.forms import ProjectForm, ProjectEditForm


@login_required
def mange(request):
    """
    项目管理
    """
    project_list = Project.objects.all()
    username = request.session.get('user', 'guest')
    return render(request, "project_list.html", {"projects": project_list, "user": username})


def add_project(request):
    """创建项目"""
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            describe = form.cleaned_data['describe']
            status = form.cleaned_data['status']
            print("sss", status, type(status))
            Project.objects.create(name=name, describe=describe, status=status)

        return HttpResponseRedirect("/project/")
    else:
        form = ProjectForm()
    return render(request, 'project_add.html', {'form': form})


def edit_project(request, pid):
    print("pid", pid)
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
        return HttpResponseRedirect("/project/")
    else:
        if pid:
            p = Project.objects.get(id=pid)
            form = ProjectEditForm(instance=p)
        else:
            form = ProjectForm()
        return render(request, 'project_edit.html', {
            'form': form, "id": pid})
