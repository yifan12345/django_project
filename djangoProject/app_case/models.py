from django.db import models

# Create your models here.
from app_manage.models import Module


class TestCase(models.Model):
    '''
    保存用例表
    '''
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=50, null=False)
    url = models.TextField("URL", null=False)
    # 1:GET, 2: POST, 3:DELETE, 4:PUT
    method = models.IntegerField("请求方法", null=False)
    header = models.TextField("请求头", null=False)
    parameter_type = models.IntegerField(
        "参数类型", null=False)  # 1：form-data 2: json
    parameter_body = models.TextField("参数内容", null=False)
    result = models.TextField("结果", null=False)
    assert_type = models.IntegerField(
        "断言类型", null=False)  # 1：包含contains 2: 相等equal
    assert_text = models.TextField("结果", null=False)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)


    def __str__(self):
        return self.name
