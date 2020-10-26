
### django实现登录注意点

在 __index.html__ 页面当中:

```html
<form action="/login_action/" method="get/post">
    <input name="username">
    <input name="password">
</form>
```

* 请求路径 login_action/
* 请求方法：get/post
* input 标签的 name属性是传参的名称

在 __views.py__ 文件中：

```python
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def login_action(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        user = auth.authenticate(
            username=username, password=password)
        if user is not None:
            auth.login(request, user)  # 验证登录
            return render(request, "project_manage.html")
        else:
            return render(request, "index.html",
                                    {"error": "用户名或者密码错误"})



@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/index/")

```

* request.POST.get("username", "") 获取POST请求的参数。
* auth.authenticate 判断用户是否存在。
* auth.login(request, user)  保留用户的登录信息。将用户session ID 写入session表
* @login_required 装饰视图函数，当前用户没有登录，该视图函数不允许访问。
* auth.logout(request)  删除用户的登录信息，将用户session ID 从session表删除
