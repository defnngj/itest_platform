from django.contrib import admin
from app_manage.models.project import Project


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'describe', "create_time"]  # 显示字段
    search_fields = ['name']  # 搜索栏
    list_filter = ['status']  # 过滤器


admin.site.register(Project, ProjectAdmin)
