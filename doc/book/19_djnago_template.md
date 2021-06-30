
### django 模板设置

默认情况下，我们需要将模板目录创建到 应用的下面，例如：

```
/app_case/templates/
```

* app_case是应用
* 模板目录必须命名为`templates`

如果要修改模板的位置命名，可以再setting.py文件中修改

```py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

```

* BACKEND 是一个指向实现了Django模板后端API的模板引擎类的带点的Python路径。内置的后端有 `django.template.backends.django.DjangoTemplates` 和 `django.template.backends.jinja2.Jinja2`

* DIRS 定义了一个目录列表，模板引擎按列表顺序搜索这些目录以查找模板源文件。

* APP_DIRS 告诉模板引擎是否应该进入每个已安装的应用中查找模板。每种模板引擎后端都定义了一个惯用的名称作为应用内部存放模板的子目录名称。（例如django为它自己的模板引擎指定的是 `templates` ，为jinja2指定的名字是`jinja2`）
