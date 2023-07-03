import json

from django.core.cache import cache
from .models import White


def get_whith():
    white_json = cache.get("rms-white-urls")
    if white_json:
        return json.loads(white_json)["whith"]

    whith = White.objects.all()
    whith_list = []
    if not whith:
        whith_list_create = [White(url="/account/login/", method="GET"), White(url="/account/login/", method="POST"),
                             White(url="/account/captcha/", method="GET"), White(url="/error404/", method="GET"),
                             White(url="/account/notpermission/", method="GET")]
        White.objects.bulk_create(whith_list_create)
        whith_list = [{'url': '/account/login/', 'method': 'GET'}, {'url': '/account/login/', 'method': 'POST'},
                      {'url': '/account/captcha/', 'method': 'GET'}, {'url': '/error404/', 'method': 'GET'},
                      {'url': '/account/notpermission/', 'method': 'GET'}]
    else:
        whith_list = [{'url': data.url, 'method': data.method} for data in whith]

    white_json = json.dumps({"whith": whith_list})
    cache.set(key="rms-white-urls", value=white_json)
    return json.loads(white_json)["whith"]


def update_whith_cache():
    whith = White.objects.all()
    whith_list = [{'url': data.url, 'method': data.method} for data in whith]
    white_json = json.dumps({"whith": whith_list})
    cache.set(key="rms-white-urls", value=white_json)
