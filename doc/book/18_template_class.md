# django 的模板划分

页面1
```HTML
<html>
<head></head>
<body>
<div>导航</div>
<div>模块1</div>
</body>

<html>
```

页面2
```HTML
<html >
<head > </head >
<body >
<div > 导航 < /div >
<div > 模块2 < /div >
</body >

<html >
```

base.html

```HTML
<html >
<head > </head >
<body >
<div > 导航 < /div >
{ % block base % }

{ % endblock % }
</body >

<html >
```

page1.html

```HTML
{ % extends "base.html" % }
{ % block base % }
    <div>模块1<div>
{ % endblock % }
```

page2.html

```HTML
{% extends "base.html" % }
{% block base % }
<div > 
模块2 

{ % block page % }
    <!--子模块-->
{ % endblock % }


< div >
{% endblock % }
```

page2-module2.html

```HTML
{% extends "page2.html" % }
{% block page % }
<div > 模块1 < div >
{% endblock % }
```

## 继承关系

* base.html
  * login.html
  * manage.html
    * project_list.html
    * project_add.html
  