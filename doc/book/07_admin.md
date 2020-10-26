

# django自带admin使用

我们可以把在 __models.py__ 中创建的表映射到admin后台进行管理。

```python
from user_app.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'describe', 'status', 'start_time','id']  #显示字段
    search_fields = ['name']   # 搜索栏
    list_filter = ['status']   # 过滤器


admin.site.register(Event, ProjectAdmin)
```

参考：https://docs.djangoproject.com/en/2.1/ref/contrib/admin/