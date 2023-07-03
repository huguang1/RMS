from django.db import models


class Logs(models.Model):
    """
     操作日志

     act_name:操作名称
     act_content:操作描述
     act_time:操作时间
     act_user:操作用户
    """

    act_name = models.CharField(max_length=32, null=False, default=None)
    act_content = models.CharField(max_length=255, null=False, default=None)
    act_time = models.DateTimeField(auto_now_add=True)
    act_user = models.ForeignKey('rmsauth.User', on_delete=models.CASCADE)

    class Meta:
        # 逆序排序
        ordering = ['-id']
