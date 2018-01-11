# coding=utf-8
import re
import json
from django.http import HttpResponse


def _ajax_return(status_code=0, msg='', data=None):
    return HttpResponse(json.dumps({
        'code': status_code,
        'msg': msg,
        'content': data,
    }))


def _ajax_success(data=None):
    return _ajax_return(0, '', data)


def _ajax_error(status_code, msg=''):
    return _ajax_return(status_code, msg)

def _is_doubtful(str):
    return len(str)>50 or bool(re.search(r'\'|"|=|\\|\/', str))
