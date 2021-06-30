from itest_platform.common import response
from app_manage.models.variable import Variable


def add_variable(request):
    """
    添加变量
    """
    if request.method == "POST":
        vid = request.POST.get("vid", "")
        key = request.POST.get("key", "")
        value = request.POST.get("value", "")
        if key == "" or value == "":
            return response(10102, "参数不能为空！")

        if vid == "0":
            Variable.objects.create(key=key, value=value)
            return response(message="创建成功")
        else:
            variable = Variable.objects.get(id=vid)
            variable.key = key
            variable.value = value
            variable.save()
            return response(message="保存成功")
    else:
        return response(10101, "请求方法错误")


def delete_variable(request):
    """
    删除变量
    """
    if request.method == "POST":
        vid = request.POST.get("vid", "")

        if vid == "":
            return response(10102, "参数不能为空！")

        variable = Variable.objects.get(id=vid)
        variable.delete()
        return response(message="删除成功")
    else:
        return response(10101, "请求方法错误")