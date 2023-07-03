import logging

from django.urls import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # 判断登录装饰器
from django.utils.decorators import method_decorator  # 类装饰器
from django.views.generic import View
from django.conf import settings

from utils import restful
from utils.pagination import get_pagination_data

from .models import Logs

logger = logging.getLogger(__name__)


# @method_decorator(login_required, name='dispatch')
class LogsView(View):
    """
    操作日志
    """

    def get(self, request):
        page = request.GET.get('p', 1)

        try:
            # 查询所有日志
            logs = Logs.objects.all()
            if logs:
                # 对logs进行分页,每页PAGE_COUNT条数据(PAGE_COUNT默认值:15)
                paginator = Paginator(logs, settings.PAGE_COUNT)
                obj_page = paginator.page(page)
                context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
                context = {'logs': obj_page, 'count': len(logs)}
                context.update(context_data)
            else:
                return render(request, 'logs/syslog.html')
        except Exception as e:
            logger.error(e)  # 日志
            return redirect(reverse('rms_syslogs:syslogs'))
        else:
            # context: logs:所以日志, conunt:日志数量
            return render(request, 'logs/syslog.html', context=context)

    def delete(self, request):
        """
        删除所有日志
        :param request:
        :return:
        """
        try:
            logs = Logs.objects.all()

            if logs:
                logs.delete()
            else:
                return restful.ok()
        except Exception as e:
            logger.error(e)
            return restful.server_error(message="日志删除失败，请刷新数据重试")
        else:
            return restful.ok()
