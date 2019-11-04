from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def login(request):
    """
    用户登录
    """
    # 返回登录页面
    if request.method == "GET":
        return render(request, "login.html")

    # 处理登录请求
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == "" or password == "":
            return render(request, "login.html", {
                "error": "用户名或密码为空！"
            })

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 记录用户的登录状态
            request.session['user'] = username
            return HttpResponseRedirect("/project/")
        else:
            return render(request, "login.html", {
                "error": "用户名或密码错误！"
            })


@login_required
def logout(request):
    """
    退出
    """
    auth.logout(request)
    return HttpResponseRedirect("/")

