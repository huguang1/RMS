from threading import Thread

from django.utils import timezone
from apps.rmslogs.models import Logs

import logging

logger = logging.getLogger(__name__)


def append_db(name, content, username):
    time_now = timezone.now()
    try:
        logs = Logs(act_name=name, act_content=content, act_user=username, act_time=time_now)
        logs.save()
    except Exception as e:
        logger.error(e)


def add_log(name, content, user):
    """
    添加日志
    :param name: 操作名称
    :param content: 操作描述
    :param user: 操作用户
    :return:
    """
    try:
        Thread(target=append_db, args=[name, content, user]).start()
    except Exception as e:
        logger.error(e)
