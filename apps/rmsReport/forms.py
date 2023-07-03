#-*- coding:utf-8 -*-
# author:无名
# datetime:2019/5/12 0012 16:49
# software: PyCharm
from django import forms

from rmsReport.models import Target
from utils.forms import FormMixin

class TargetForm(forms.Form,FormMixin):
    group_count = forms.IntegerField(error_messages={"invalid":"组员数量必须是数字"})
    new_resume = forms.IntegerField(error_messages={"invalid":"新增简历数量必须是数字"})
    admit_count = forms.IntegerField(error_messages={"invalid":"录取数量必须是数字"})
    entry_count = forms.IntegerField(error_messages={"invalid":"入职数量必须是数字"})

