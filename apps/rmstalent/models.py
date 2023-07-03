from django.db import models

from apps.rmsManager.models import Company
from apps.rmsManager.models import Job
from apps.rmsManager.models import RecruitmentWay


class Talent(models.Model):
    """
    人才库
    name: 姓名
    gender: 性别
    remark: 备注
    channel：招聘途径
    user: 招聘员
    admit_company: 录取公司
    region: 区域
    expect_job: 期待岗位
    admit_job：录取岗位
    interviewed_company: 面试过的公司, 多对多关联 Company
    resume_url: 简历url
    status: 状态{}
    entry_date:入职时间
    underway: 是否进行中
    """

    Status_Choices = (
        (1, '待面试'),
        (2, '待入职'),
        (3, '办理签证'),
        (4, '待分配'),
        (5, '到岗'),
        (6, '跳票'),
        (7, '已放弃'),
        (8, '离职')
    )

    name = models.CharField(max_length=64, null=False, blank=False)
    gender = models.BooleanField(default=True, null=False)
    remark = models.CharField(max_length=255, null=True, blank=True)
    resume_url = models.UUIDField(null=True)
    status = models.SmallIntegerField(choices=Status_Choices, null=False)
    channel = models.ForeignKey(to=RecruitmentWay, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(to="rmsauth.User", blank=True, null=True, on_delete=models.SET_NULL)
    region = models.ForeignKey(to="Region", blank=True, null=True, on_delete=models.SET_NULL)
    job = models.ForeignKey(to=Job, blank=True, null=True, on_delete=models.SET_NULL)
    expect_job = models.CharField(max_length=128, blank=True, null=True)
    entry_date = models.DateTimeField(blank=True, null=True)
    underway = models.BooleanField(default=False)  # 录取了没入职--进行中
    admit_date = models.DateTimeField(blank=True, null=True)
    interviewed_company = models.ManyToManyField(to="InterviewedCompany")
    admit_company = models.ForeignKey(to=Company, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'rms_talent'
        ordering = ['id']


class InterviewedCompany(models.Model):
    name = models.CharField(max_length=64, null=False)

    class Meta:
        db_table = 'rms_interviewed_company'
        ordering = ['id']


class Region(models.Model):
    """
    区域: 中国，越南。。。。
    """
    name = models.CharField(max_length=16, null=False, blank=False)

    class Meta:
        db_table = 'rms_region'
        ordering = ['id']


class Interview(models.Model):
    """
    面试
    number: 第几次面试
    date: 面试时间
    status: 是否通过
    desc: 面试描述
    """

    number = models.IntegerField(default=1, null=False)
    date = models.DateTimeField(null=False)
    status = models.BooleanField(null=False, default=False)
    desc = models.CharField(max_length=128, null=False)

    class Meta:
        db_table = "rms_interview"
        ordering = ['id']


class Schedule(models.Model):
    """
    进度

    """
    name = models.CharField(max_length=64, null=False, blank=False)

    class Meta:
        db_table = "rms_schedule"
        ordering = ['id']


class Status(models.Model):
    code = models.SmallIntegerField()
    time = models.DateTimeField(auto_now_add=True)
    talent = models.ForeignKey(to="Talent", on_delete=models.CASCADE, related_name="status_list")
