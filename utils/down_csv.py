# import csv
# import random
#
# from datetime import datetime
# from datetime import timedelta
# from datetime import timezone
# from django.http import StreamingHttpResponse


class Echo:
    """
    定义一个可以执行写操作的类,以后调用csv.writer的时
    候,就会执行这个方法
    """
    
    def write(self, value):
        return value


# def large_csv(request):
#     # 创建时区UTC+8:00
#     tz_utc_8 = timezone(timedelta(hours=8))
#     # 获取时区UTC+8:00的当前时间
#     date_now = datetime.now(tz_utc_8)
#     # 格式化成字符串，用作文件名, 避免文件名冲突
#     filename = date_now.strftime("%Y%m%d%H%M%S") + '_' + ''.join(random.sample('0123456789', 5)) + '.csv'
#     # 数据 ([],[],[],[])
#     rows = (["Row {}".format(idx), str(idx)] for idx in range(500))
#
#     pseudo_buffer = Echo()
#     writer = csv.writer(pseudo_buffer)
#     response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
#     response['Content-Disposition'] = 'attachment;filename="%s"' % filename
#     return response

