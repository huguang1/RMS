from django.core.paginator import Paginator
from django.conf import settings


# paginator: Paginator对象, page_obj: 当前页的对象, around_count: 当前页左右两边的页码（左边显示多少页,右边显示多少页）
def get_pagination_data(paginator, page_obj, around_count=2):
    current_page = page_obj.number
    num_pages = paginator.num_pages
    
    left_has_more = False
    right_has_more = False
    
    if current_page <= around_count + 2:
        left_pages = range(1, current_page)
    else:
        left_has_more = True
        left_pages = range(current_page - around_count, current_page)
    
    if current_page >= num_pages - around_count - 1:
        right_pages = range(current_page + 1, num_pages + 1)
    else:
        right_has_more = True
        right_pages = range(current_page + 1, current_page + around_count + 1)
    
    return {
        # left_pages：代表的是当前这页的左边的页的页码
        'left_pages': left_pages,
        # right_pages：代表的是当前这页的右边的页的页码
        'right_pages': right_pages,
        # 当前是第几页
        'current_page': current_page,
        # 左边是否显示‘...’
        'left_has_more': left_has_more,
        # 右边是否显示‘...’
        'right_has_more': right_has_more,
        # 总共有多少页
        'num_pages': num_pages
    }


"""
# 对newses进行分页,每页2条数据
paginator = Paginator(newses, 2)
page_obj = paginator.page(page) # 第几页
# 分页按钮展示计算
get_pagination_data(paginator, page_obj)
"""


# paginator: Paginator对象, page_obj: 当前页的对象, around_count: 当前页左右两边的页码（左边显示多少页,右边显示多少页）
def get_pagination_json_data(paginator, page_obj, around_count=2):
    current_page = page_obj.number
    num_pages = paginator.num_pages
    
    left_has_more = False
    right_has_more = False
    
    if current_page <= around_count + 2:
        left_pages = range(1, current_page)
    else:
        left_has_more = True
        left_pages = range(current_page - around_count, current_page)
    
    if current_page >= num_pages - around_count - 1:
        right_pages = range(current_page + 1, num_pages + 1)
    else:
        right_has_more = True
        right_pages = range(current_page + 1, current_page + around_count + 1)
    
    return {
        # left_pages：代表的是当前这页的左边的页的页码
        'left_pages': [i for i in left_pages],
        # right_pages：代表的是当前这页的右边的页的页码
        'right_pages': [i for i in right_pages],
        # 当前是第几页
        'current_page': current_page,
        # 左边是否显示‘...’
        'left_has_more': left_has_more,
        # 右边是否显示‘...’
        'right_has_more': right_has_more,
        # 总共有多少页
        'num_pages': num_pages
    }


# 分页处理
def get_page_context(obj, page, kwargs=None):
    paginator = Paginator(obj, settings.PAGE_COUNT)
    obj_page = paginator.page(page)
    context_data = get_pagination_data(paginator=paginator, page_obj=obj_page)
    context = {'data': obj_page}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        context.update(kwargs)
    context.update(context_data)
    
    return context


# 分页处理
# def get_page_json_context(obj, page, kwargs=None):
#     paginator = Paginator(obj, settings.PAGE_COUNT)
#     obj_page = paginator.page(page)
#     context_data = get_pagination_json_data(paginator=paginator, page_obj=obj_page)
#     context = {'data': obj_page}
#     if kwargs and isinstance(kwargs, dict) and kwargs.keys():
#         context.update(kwargs)
#     context.update(context_data)
#     return context
