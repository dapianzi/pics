# coding=utf-8
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


def _remote_addr(request):
    """
    get remote address
    :param request:
    :return:
    """
    return '127.0.0.1'


def _is_doubtful(str, type='ip'):
    return False
