
### django设置本地静态文件（css/js/image）

参考：
https://docs.djangoproject.com/en/2.1/howto/static-files/

1、__settting.py__ 文件设置

```py
STATIC_URL = '/static/'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

```

BASE_DIR 指定为当前项目的根目录下面，例如：```test_platform/```
，创建静态文件目录为：```test_platform/static/```

2、创建static/目录，结构如下：

```shell
test_platform/static/
├─────────────── css/
│                ├── bootstrap.min.css
│                └── signin.css
├─────────────── js/
│                ├── bootstrap.js
│                └── bootstrap.min.js
├─────────────── fonts/
├─────────────── img/
```

3、在HTML文件中引用静态资源。

```HTML
<!-- 引用本地样式 -->
  {% load static %}
  <link rel="stylesheet" type="text/css" href="{% static "css/bootstrap.min.css" %}">
  <link rel="stylesheet" type="text/css" href="{% static "css/signin.css" %}">

```
