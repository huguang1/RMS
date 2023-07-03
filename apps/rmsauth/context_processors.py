# 模板上下文处理
def front_menus(request):
    context = {}
    if request.user.is_authenticated:
        context['menus'] = request.session.get("rms_menu_list_key")
    return context
