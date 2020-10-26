
### Django 创建表：

创建数据库表：
```python
from django.db import models


class Project(models.Model):
    """
    项目表
    """
    name = models.CharField("名称", max_length=100, blank=False, default="")
    describe = models.TextField("描述", default="")
    status = models.BooleanField("状态：", default=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name


class Module(models.Model):
    """
    模块表
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100, blank=False, default="")
    describe = models.TextField("描述", default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
```

数据类型查看 ```C:\Python37\Lib\site-packages\django\db\models\fields\__init__.py```


__参数说明__

* max_length 最大长度。
* default 默认值。
* null 针对数据库，null=True 表示该字段允许为空。
* blank 针对表单，blank=True 表示表单该字段可以为空。 
* auto_now 每次更新数据，都会获取最新时间更新。
* auto_now_add 当数据被创建时，获取最新时间更新。
* on_delete 指定关联数据， models.CASCADE 表示删除关联数据时，与之关联也删除。

### 数据库表操作：

* 创建
```python
Project.objects.create(name="项目", describe="描述")
```

* 查询
```python
Project.objects.all()
Project.objects.get(pk=1)
Project.objects.filter(status=1)
Project.objects.filter(name__contains='项目')
```

* 更新
```python
g = Project.objects.get(name='xxx测试项目')
g.status=0
g.save()

Project.objects.select_for_update().filter(name__contains='项目').update(describe='')
```

* 删除
```python
Project.objects.get(name='xxx测试项目').delete()
```

ORM优势：
* 更简单
* 更统一
