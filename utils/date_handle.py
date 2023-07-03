import datetime
from django.utils.timezone import get_current_timezone
from django.utils import timezone

# 字符串转日期 "年-月-日"
def str_to_date(str_date):
    year_str, mon_str, day_str = str_date.split('-')
    return datetime.date(int(year_str), int(mon_str), int(day_str))


# 字符串转时间 "年-月-日 时:分:秒"
def str_to_datetime(str_datetime):
    date_str, time_str = str_datetime.split(' ')
    year_str, mon_str, day_str = date_str.split('-')
    hour_str, minute_str, second_str = time_str.split(':')
    result = datetime.datetime(year=int(year_str), month=int(mon_str), day=int(day_str), hour=int(hour_str),
                               minute=int(minute_str), second=int(second_str), tzinfo=get_current_timezone())
    return result


# 判断字符串
def is_string(obj):
    try:
        obj.lower() + obj.title() + obj + ""
    except:
        return False
    else:
        return True


# 获取昨天日期
def get_yesterday(str_date):
    if is_string(str_date):
        today = str_to_date(str_date)
    else:
        today = str_date
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return yesterday


now = timezone.datetime.now()
tomorrow = (now + datetime.timedelta(days=1)).replace(tzinfo=get_current_timezone())

time_now = {"year": now.year, "month":now.month, "day": now.day}
time_tomorrow = {"year": tomorrow.year, "month":tomorrow.month}


# 判断时间格式是否符合标准
def validate_time(date_text):
    '''
    :param date_text: 时间字符串
    :return:
    '''
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("时间格式不正确, 应该是YYYY-MM-DD")


# 判断是否是月末
def validate_end_month():

    return True if tomorrow.day == 1 else False

# 判断有多少个月.如果是当前年份,月数为当前月,如果是以前年份,则为12个月
def year_month(date):
    '''
    :param date: 年份
    :return:
    '''
    return  now.month if date == now.year else 12

