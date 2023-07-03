# import functools
# from utils import restful
# from apps.stock.models import TransactionHour
# from django.utils import timezone
# import logging
# import datetime
#
# logger = logging.getLogger(__name__)
#
#
# # 判断会员有没有登录, 是否在活动时间,是否维护,是否关闭
# def index_login_check(func):
#     @functools.wraps(func)
#     def wrapper(request, *args, **kwargs):
#         if request.session.get('IS_SIGIN', ''):
#             return func(request, *args, **kwargs)
#         else:
#             return restful.unauth(message="请先登录")
#
#     return wrapper
#
#
# def time_limit(func):
#     @functools.wraps(func)
#     def wrapper(request, *args, **kwargs):
#         current_time = timezone.now()
#         try:
#             trans = TransactionHour.objects.get(id=1)
#         except Exception as e:
#             logger.error(e)
#             return restful.server_error(message="系统维护中....")
#         else:
#             start_time = trans.start_time
#             end_time = trans.end_time
#             start_a = trans.start_a
#             end_a = trans.end_a
#             # start_b = trans.start_b
#             # end_b = trans.end_b
#             is_maintain = trans.is_maintain
#             maintain_desc = trans.maintain_desc
#             close_desc = trans.close_desc
#             if is_maintain:
#                 return restful.server_error(message=maintain_desc)
#             else:
#                 if (start_time <= current_time) and (current_time <= end_time):
#                     tz_utc_8 = datetime.timezone(datetime.timedelta(hours=8))
#                     # 获取时区UTC+8:00的当前时间
#                     date_now = datetime.datetime.now(tz_utc_8)
#                     c_time = date_now.time()
#                     if (start_a <= c_time) and (c_time <= end_a):
#                         return func(request, *args, **kwargs)
#                     else:
#                         return restful.server_error(message="不在活动时间范围")
#                 else:
#                     return restful.server_error(message=close_desc)
#
#     return wrapper
