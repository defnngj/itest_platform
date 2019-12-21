from django.db import models


class Variable(models.Model):
    """
    公共变量表
    """
    key = models.CharField("变量key", max_length=100, null=False, default="")
    value = models.TextField("变量value", default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.key


