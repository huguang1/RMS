import os
import uuid
import logging
from datetime import datetime
from datetime import timezone
from datetime import timedelta

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator
from django.http import QueryDict
from django.shortcuts import redirect
from django.db.models import Q

from utils import restful
from utils.pagination import get_pagination_data

from .models import Talent
from .models import Region
from .models import Schedule
from .models import Status
from .models import InterviewedCompany
from . import common
from .serializers import TalentSerializers

from apps.rmsManager.models import RecruitmentWay
from apps.rmsManager.models import Job

logger = logging.getLogger(__name__)


class UploadView(View):
    """
    # 上传文件接口
    """

    def post(self, request):
        # 接收文件对象
        file = request.FILES.get('file')
        # 获取文件扩展名
        ex_name = file.name.split('.')[-1]
        if ex_name != 'pdf':
            return restful.params_error(message="必须是pdf文档，后缀名为.pdf")
        # 创建时区UTC+8:00
        tz_utc_8 = timezone(timedelta(hours=8))
        # 获取时区UTC+8:00的当前时间
        date_now = datetime.now(tz_utc_8)
        uuid_name = uuid.uuid5(uuid.NAMESPACE_DNS, date_now.strftime("%Y%m%d%H%M%S"))
        # 文件名
        name = str(uuid_name) + '.' + ex_name
        # 文件保存到指定目录
        with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as fp:
            for chunk in file.chunks():
                fp.write(chunk)
        # 返回文件名称
        return restful.result(data={'name': uuid_name})


class TalentView(View):
    def get(self, request):
        try:
            if request.user.is_superuser or request.user.is_ordinaryadmin:
                talents = Talent.objects.select_related('user', 'region', 'channel').all()
            else:
                talents = Talent.objects.select_related('user', 'region', 'channel').filter(user=request.user)
            paginator = Paginator(talents, settings.PAGE_COUNT)
            obj_page = paginator.page(1)
            context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
            context = {'data': obj_page, 'count': len(talents)}
            context.update(context_data)
            return render(request, 'talent/rms_talent.html', context=context)
        except Exception as e:
            logger.error(e)
            return redirect('/error404/')


class TalentListView(View):
    def get(self, request):
        try:
            page = int(request.GET.get('p', 1))
        except:
            page = 1
        # 一页显示多少条数据
        one_page_count = settings.PAGE_COUNT
        start = (page - 1) * one_page_count
        end = start + one_page_count

        talents = Talent.objects.select_related('user', 'region', 'channel').all()
        # 总共有多少条数据
        count = len(talents)
        # 一页数据
        data = talents[start:end]
        # 序列化
        serializer = TalentSerializers(data, many=True)
        # 序列化后的数据
        tmp_data = serializer.data

        return restful.result(data={"data": tmp_data, "count": count, "page_count": one_page_count})


class TalentDetailView(View):
    def get(self, request, data=0):
        try:
            talent_id = data
            talent = Talent.objects.get(Q(id=talent_id) & Q(user=request.user))
            return render(request, 'talent/rms_talent_detail.html', context={"data": talent})
        except Exception as e:
            logger.error(e)
            return redirect('/error404/')


class TalentEntryInfoView(View):
    def get(self, request):
        regions = Region.objects.all()
        channels = RecruitmentWay.objects.all()
        status = Talent.Status_Choices
        interviewed_companies = InterviewedCompany.objects.all()
        jobs = Job.objects.all()
        context = {"regions": regions, "channels": channels, "statuses": status, "jobs": jobs,
                   "interviewed_companies": interviewed_companies}
        return render(request, 'talent/rms_talent_entry_info.html', context=context)

    # 添加人才
    def post(self, request):
        name = request.POST.get('name', '')
        try:
            gender = int(request.POST.get('gender'))
        except:
            gender = 1
        try:
            channel = int(request.POST.get('channel'))
        except:
            channel = 0
        try:
            region = request.POST.get('region')
        except:
            region = 0
        try:
            status = int(request.POST.get('status'))
        except:
            status = 1
        resume_uuid = request.POST.get('resume_uuid', '')
        interviewed = request.POST.getlist('interviewed')
        expect_job = request.POST.get('expect_job', '')
        remark = request.POST.get('remark', '')

        kwags = dict()
        if not name:
            return restful.params_error(message="请输入姓名")
        if not channel:
            return restful.params_error(message="请选择招聘途径")
        if not region:
            return restful.params_error(message="请选择区域")
        if not status:
            return restful.params_error(message="请选择人才状态")
        kwags.update({"name": name, "status": status, "user": request.user})
        if gender:
            kwags.update({"gender": True})
        else:
            kwags.update({"gender": False})

        try:
            channel_obj = RecruitmentWay.objects.get(id=channel)
            region_obj = Region.objects.get(id=region)
            kwags.update({"channel": channel_obj, "region": region_obj})
        except Exception as e:
            logger.error(e)
            return restful.params_error(message="区域、招聘途径没有选择")
        if resume_uuid:
            kwags.update({"resume_url": resume_uuid})
        if remark:
            kwags.update({"remark": remark})
        if expect_job:
            kwags.update({"expect_job": expect_job})

        try:
            talent = Talent.objects.create(**kwags)
            Status.objects.create(code=status, talent=talent)
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="人才信息录入失败，请刷新数据重试")

        try:
            common.chang_status(talent)
        except:
            pass
        if interviewed:
            try:
                interviewed_int = [int(interviewe) for interviewe in interviewed]
                intervieweds = InterviewedCompany.objects.filter(id__in=interviewed_int)
                talent.interviewed_company.add(*intervieweds)
            except:
                pass
        return restful.ok()


class RegionView(View):
    """
    添加区域接口
    """

    def post(self, request):
        name = request.POST.get('name')
        if not name:
            return restful.params_error(message="请输入区域名称")
        try:
            region = Region.objects.create(name=name)
            return restful.result(data={"id": region.id, "name": region.name})
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="数据保存不成功，请刷新重试")


class InterviewedCompanyView(View):
    """
    添加应聘过的公司接口
    """

    def post(self, request):
        name = request.POST.get('name')
        if not name:
            return restful.params_error(message="请输入公司名称")
        try:
            interviewed = InterviewedCompany.objects.create(name=name)
            return restful.result(data={"name": interviewed.name})
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="数据保存不成功，请刷新重试")
