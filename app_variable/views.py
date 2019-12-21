from django.shortcuts import render
from itest_platform.common import response
from app_variable.models import Variable


def variable_manage(request):
    """
    变量管理
    """
    if request.method == "GET":
        variables = Variable.objects.all()
        return render(request, "variable/list.html", {"variables": variables})
