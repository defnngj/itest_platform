from django.db import models


class TestTask(models.Model):
    """
    测试任务表
    """
    name = models.CharField("名称", max_length=100, blank=False, default="")
    describe = models.TextField("描述", default="")
    status = models.IntegerField("状态", default=0)  # 未执行、执行中、执行完成、排队中
    cases = models.TextField("关联用例", default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name


class TestResult(models.Model):
    """
    测试结果表
    """
    name = models.CharField("名称", max_length=100, blank=False, default="")
    task = models.ForeignKey(TestTask, on_delete=models.CASCADE)
    error = models.IntegerField("错误用例", default=0)
    failure = models.IntegerField("失败用例", default=0)
    skipped = models.IntegerField("跳过用例", default=0)
    tests = models.IntegerField("总用例数", default=0)
    run_time = models.FloatField("运行时长", default=0)
    result = models.TextField("详细", default="")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    def __str__(self):
        return self.name
