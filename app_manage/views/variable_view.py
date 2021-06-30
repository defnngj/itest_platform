from django.shortcuts import render
from app_manage.models.variable import Variable


def variable_manage(request):
    """
    变量管理
    """
    variables = Variable.objects.all()
    return render(request, "variable/list.html", {"variables": variables})
