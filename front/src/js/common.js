function Common() {

}


//获取url中的参数
Common.prototype.getUrlParam = function (name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
    var r = window.location.search.substr(1).match(reg);  //匹配目标参数
    if (r != null) return unescape(r[2]);
    return null; //返回参数值
};

// 生成UUID
Common.prototype.generateUUID = function () {
    var d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid_code = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid_code;
};


/*
around_count: 当前页左右两边的页码
page_count: 一页显示多少条数据
current_page: 当前页
count: 总共有多少条数据
*/
Common.prototype.paginationHandle = function (around_count, current_page, page_count, count) {
    // left_has_more 左边是否显示‘...’
    // right_has_more 右边边是否显示‘...’
    // left_pages 当前这页的左边的页的页码
    // right_pages 当前这页的右边的页的页码
    // num_pages 总共有多少页数据
    var left_has_more, right_has_more, left_pages, right_pages, num_pages;
    left_has_more = false;
    right_has_more = false;
    left_pages = [];
    right_pages = [];

    num_pages = Math.ceil(count / page_count);

    if (current_page <= around_count + 2) {
        left_has_more = false;
        for (var p=1; p<current_page; p++) {
            left_pages.push(p);
        }
    } else {
        left_has_more = true;
        for (var rp=(current_page - around_count); rp<(current_page); rp++)
        {
            left_pages.push(rp);
        }
    }

    if (current_page >= (num_pages - around_count - 1)) {
        right_has_more = false;
        for (var lp = (current_page + 1); lp<(num_pages + 1); lp++){
            right_pages.push(lp);
        }
    } else {
        right_has_more = true;
        for (var l = (current_page + 1); l<(current_page + around_count + 1); l++){
            right_pages.push(l);
        }
    }

    return {
        //left_pages：代表的是当前这页的左边的页的页码
        'left_pages': left_pages,
        //right_pages：代表的是当前这页的右边的页的页码
        'right_pages': right_pages,
        //当前是第几页
        'current_page': current_page,
        //左边是否显示‘...’
        'left_has_more': left_has_more,
        //右边是否显示‘...’
        'right_has_more': right_has_more,
        //总共有多少页
        'num_pages': num_pages
    }

};

var common = new Common();
