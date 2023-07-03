from django.db import models
from apps.rmsauth.models import User, Group
import django.utils.timezone as timezone


# Create your models here.
class Company(models.Model):
    cooperation_models = models.CharField(max_length=32, verbose_name="合作形式")
    code = models.CharField(max_length=32, verbose_name="公司代码")
    area = models.CharField(max_length=32, verbose_name="区域")
    block = models.CharField(max_length=32, verbose_name="大楼")
    floor = models.CharField(max_length=32, verbose_name="楼层")
    hr = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True, related_name="companys")
    addr = models.CharField(max_length=128, verbose_name="地址")
    rebate = models.TextField(verbose_name="返拥")

    class Meta:
        verbose_name = "公司"
        verbose_name_plural = "公司"
        db_table = "rms_company"
        ordering = ["-id"]


job_type_tuple = ((1, "国内"), (2, "外籍"))


class JobDemand(models.Model):
    company = models.ForeignKey(to="Company", on_delete=models.CASCADE)
    job_type = models.IntegerField(choices=((1, "国内"), (2, "外籍")), default=1)
    job = models.ForeignKey(to="Job", verbose_name="岗位", on_delete=models.CASCADE)
    nums = models.CharField(max_length=32, verbose_name="需求数量")
    work = models.TextField(verbose_name="岗位职责")
    need = models.TextField(verbose_name="任职资格")
    sex = models.IntegerField(choices=((1, "男"), (2, "女"), (3, "男女不限")), verbose_name="性别")
    edu = models.CharField(verbose_name="学历", max_length=64)
    work_years = models.CharField(max_length=64, verbose_name="工作年限")
    essential_condition = models.TextField(verbose_name="必备条件")
    recruitment_way = models.CharField(verbose_name="招聘渠道", max_length=64)
    probation_salary = models.CharField(verbose_name="试用期薪资", max_length=64)
    salary = models.CharField(verbose_name="薪资", max_length=64)
    salary_method = models.TextField(verbose_name="薪资发放方式")
    performance = models.TextField(verbose_name="提成绩效")
    work_time = models.CharField(max_length=64, verbose_name="工作时间")
    holiday = models.CharField(verbose_name="每月休假", max_length=64)
    job_subsidy = models.TextField(verbose_name="岗位补贴")
    life_subsidy = models.TextField(verbose_name="生活补贴")
    dorm = models.CharField(max_length=64, verbose_name="宿舍条件")
    welfare = models.TextField(verbose_name="其他福利")
    note = models.TextField(verbose_name="备注")
    update_time = models.DateTimeField(verbose_name="更新时间", default=timezone.now)

    def sexList(self):
        return ["男", "女", "男女不限"]

    class Meta:
        verbose_name = "岗位要求"
        verbose_name_plural = "岗位要求"
        db_table = "rms_jobdemand"
        ordering = ["-id"]


class UrgencyJobDemand(models.Model):
    hr = models.ForeignKey(to=User, on_delete=models.SET_NULL, verbose_name="对接人", blank=True, null=True)
    job = models.ForeignKey(to="Job", verbose_name="岗位", on_delete=models.CASCADE)
    rebate = models.CharField(max_length=64, verbose_name="返拥")
    work = models.TextField(verbose_name="岗位职责")
    need = models.TextField(verbose_name="任职资格")
    sex = models.IntegerField(choices=((1, "男"), (2, "女"), (3, "男女不限")), verbose_name="性别")
    edu = models.CharField(verbose_name="学历", max_length=64)
    essential_condition = models.TextField(verbose_name="必备条件")
    salary = models.CharField(verbose_name="薪资", max_length=64)
    performance = models.TextField(verbose_name="提成绩效")
    work_time = models.CharField(max_length=64, verbose_name="工作时间")
    work_addr = models.CharField(max_length=64, verbose_name="工作地点")
    status = models.CharField(max_length=64, verbose_name="状态")
    note = models.TextField(verbose_name="备注")

    def sexList(self):
        return ["男", "女", "男女不限"]

    class Meta:
        verbose_name = "限时悬赏"
        verbose_name_plural = "限时悬赏"
        db_table = "rms_urgencyjobdemand"
        ordering = ["-id"]


class Job(models.Model):
    name = models.CharField(max_length=32, verbose_name="岗位名称")

    class Meta:
        ordering = ["-id"]


class RecruitmentWay(models.Model):
    name = models.CharField(max_length=64, verbose_name="渠道名")
    link_man = models.CharField(max_length=32, verbose_name='联系人')
    contact_way = models.CharField(max_length=64, verbose_name="联系方式")

    class Meta:
        verbose_name = "中介"
        verbose_name_plural = "中介"
        ordering = ["-id"]
