from django.db import models
from app_manage.models import Module


class TestCase(models.Model):
    """
    测试用例表
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50, null=False)
    url = models.TextField("URL", null=False)
    method = models.IntegerField("请求方法", null=False) # 1:GET, 2: POST, 3:DELETE, 4:PUT
    header = models.TextField("请求头", null=False)
    parameter_type = models.IntegerField("参数类型", null=False)  # 1：form-data 2: json
    parameter_body = models.TextField("参数内容", null=False)
    result = models.TextField("结果", null=False)
    assert_type = models.IntegerField("断言类型", null=False)  # 1：包含contains 2: 匹配mathches
    assert_text = models.TextField("结果", null=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
