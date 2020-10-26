
### manage常用命令

```shell

# 创建项目
$ django-admin startproject mysite

# 创建应用
$ python manage.py startapp polls

# 运行项目
$ python manage.py runserver

# 生成数据库同步文件
$ python manage.py makemigrations polls

# 执行数据库同步
$ python manage.py migrate

# djang shell 模式
$ python manage.py shell

# 创建超级管理账号
$ python manage.py createsuperuser

# 运行django单元测试
$ python manage.py test

```

### django MTV模型

* M : models，django 封装了ORM，免于直接操作数据库。

* T : templates， django自带模板语言，可以在HTML中处理数据的展示。

* V : views， 在models和templates之间处理数据。

### django 简单处理流程

1、浏览器URL：http://127.0.0.1:8000/index/

2、__urls.py__ 文件中匹配路径 __/index/__

```python
path('index/', views.index),
```

3、在 __views.py__ 文件中定义 __index()__ 函数，将 __index.html__ 文件返回给客户端浏览器

```python
def index(request):
    return render(request, "index.html")

```
