from django import forms
from utils.forms import FormMixin


class CompanyFrom(forms.Form, FormMixin):
    """
    公司信息编辑表
    """
    cooperation_models = forms.CharField(max_length=32, required=True,
                                         error_messages={'required': "请输入合作形式", "max_length": "合作形式不能超过32个字符"})
    code = forms.CharField(max_length=32, required=True,
                           error_messages={'required': "请输入公司代码", "max_length": "公司代码不能超过32个字符"})
    area = forms.CharField(max_length=32, required=True,
                           error_messages={'required': "请输入区域", "max_length": "区域不能超过32个字符"})
    block = forms.CharField(max_length=32, required=True,
                            error_messages={'required': "请输入大楼名", "max_length": "大楼名不能超过32个字符"})
    floor = forms.CharField(max_length=32, required=True,
                            error_messages={'required': "请输入楼层", "max_length": "楼层不能超过32个字符"})
    addr = forms.CharField(max_length=128, required=True,
                           error_messages={'required': "请输入地址", "max_length": "地址不能超过64个字符"})


class JobDemandForm(forms.Form, FormMixin):
    probation_salary = forms.CharField(max_length=64, required=True,
                                       error_messages={'required': "请输入试用期薪资", "max_length": "试用期薪资不能超过64个字符"})
    salary = forms.CharField(max_length=64, required=True,
                             error_messages={'required': "请输入薪资", "max_length": "薪资试用期薪资不能超过64个字符"})
    work_time = forms.CharField(max_length=64, required=True,
                                error_messages={'required': "请输入工作时间", "max_length": "工作时间不能超过64个字符"})
    holiday = forms.CharField(max_length=64, required=True,
                              error_messages={'required': "请输入每月休假", "max_length": "每月休假不能超过64个字符"})
    nums = forms.CharField(max_length=32,required=True, error_messages={'required': "请输入招聘数量", "max_length": "需求数量不能超过32个字符"})
    edu = forms.CharField(max_length=64, required=True,error_messages={'required': "请输入学历", "max_length": "学历不能超过64个字符"})
    work_years = forms.CharField(max_length=64, required=True,error_messages={'required': "请输入工作年限", "max_length": "工作年限不能超过64个字符"})
    recruitment_way = forms.CharField(max_length=64,required=True,
                                      error_messages={'required': "请输入每月招聘渠道", "max_length": "招聘渠道不能超过64个字符"})
    dorm = forms.CharField(max_length=64,required=True, error_messages={'required': "请输入每住宿条件", "max_length": "宿舍条件不能超过64个字符"})


class UrgencyJobDemandForm(forms.Form, FormMixin):
    edu = forms.CharField(max_length=64, required=True,error_messages={'required': "请输入学历", "max_length": "学历不能超过64个字符"})
    work_time = forms.CharField(max_length=64, required=True,
                                error_messages={'required': "请输入工作时间", "max_length": "工作时间不能超过64个字符"})
    work_addr = forms.CharField(max_length=64, required=True,
                                error_messages={'required': "请输入工作地点", "max_length": "工作地点不能超过64个字符"})
    status = forms.CharField(max_length=64, required=True,
                             error_messages={'required': "请输入状态", "max_length": "状态不能超过64个字符"})
    rebate = forms.CharField(max_length=64, required=True,error_messages={'required': "请输入返佣", "max_length": "返佣不能超过64个字符"})
    salary = forms.CharField(max_length=64,required=True, error_messages={'required': "请输入返佣", "max_length": "返佣不能超过64个字符"})


class RecruitmentWayForm(forms.Form, FormMixin):
    name = forms.CharField(max_length=64, required=True,
                           error_messages={'required': "请输入渠道名", "max_length": "渠道名不能超过64个字符"})
    link_man = forms.CharField(max_length=32, required=True,
                               error_messages={'required': "请输入联系人", "max_length": "联系人不能超过64个字符"})
    contact_way = forms.CharField(max_length=64, required=True,
                                  error_messages={'required': "请输入联系方式", "max_length": "联系方式不能超过64个字符"})


class JobFrom(forms.Form, FormMixin):
    name = forms.CharField(max_length=32, required=True,
                           error_messages={'required': "请输入岗位名称", "max_length": "岗位名称不能超过32个字符"})
