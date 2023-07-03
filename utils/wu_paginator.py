from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class WuPaginator(Paginator):
    def __init__(self, current_page, max_page_num, *args, **kwargs):
        """
        :param current_page: 当前页
        :param max_page_num: 最多显示的页码个数
        :param args:
        :param kwargs:
        一般传入4个参数:current_page,max_page_num,object_list(展示对象列表),per_page(每页显示的对象数量)
        """
        self.current_page = int(current_page)
        self.max_page_num = max_page_num
        super().__init__(*args, **kwargs)


    def page_num_range(self):
        part = int(self.max_page_num / 2)
        start = max(1, self.current_page - part)
        end = min(self.num_pages + 1, start + self.max_page_num)
        return range(start,end)

    def get_paginator(self):
        try:
            posts = self.page(self.current_page)
        except PageNotAnInteger:
            posts = self.page(1)
        except EmptyPage:
            posts = self.page(self.num_pages)
        return posts
