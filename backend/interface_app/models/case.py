from django.db import models
from interface_app.models import Module


class TestCase(models.Model):
    """
    测试用例表
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50, null=False)
    url = models.TextField("URL", null=False)
    method = models.CharField("请求方法", max_length=10, null=False)  # GET/POST/ DELETE /PUT
    header = models.TextField("请求头", null=True, default="{}")
    params_type = models.CharField("参数类型", max_length=10, null=False)  # GET: params POST: form/json
    params_body = models.TextField("参数内容", null=True, default="{}")
    result = models.TextField("结果", null=True, default="{}")
    assert_type = models.CharField("断言类型", max_length=10, null=True)  # include/ equal
    assert_text = models.TextField("结果", null=True, default="{}")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return self.name
