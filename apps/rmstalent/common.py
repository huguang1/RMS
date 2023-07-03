import logging

from .models import Status

logger = logging.getLogger(__name__)


# 状态
def chang_status(talent):
    try:
        status_talent = talent.status
        if status_talent in [2, 3, 4]:
            talent.underway = True
            talent.save()
        status = Status.objects.get(talent=talent)
        status.code = status_talent
        status.save()
    except Exception as e:
        logger.error(e)
        raise ValueError(e)
