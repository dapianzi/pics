from django.shortcuts import render
from django.views.generic import TemplateView,View

from pics.utils import _ajax_error,_ajax_success,_remote_addr,_is_doubtful
from . import models as spider_models
# Create your views here.

class IndexView(View):
    """
    首页搜索
    """
    template_name = 'spider/index.html'
    ip = ''

    def get(self, request, *args, **kwargs):
        context = dict()
        context['title'] = 'What can I do for you?'
        context['types'] = spider_models.ContentType.objects.all()
        keyword = request.GET.get('keyword')
        type_id = request.GET.get('type')
        if len(keyword) >= 2:

            context['keyword'] = keyword
            context['type_id'] = type_id
            return context
        else:
            context['err_msg'] = '搜索关键词不能少于2个字哦'
            return render(
                request, self.template_name, context
            )

    def _is_blocked(self):
        block = spider_models.BlackList.objects.get(ip=self.ip)
        return True if block is not None else False

    def _recordSearch(self, content):
        doubtful = _is_doubtful(content)
        search = spider_models.SearchRecord(ip=self.ip, content=content, is_doubtful=doubtful)


class GetItem(View):
    """
    拉取结果
    """
    def post(self, request, *args, **kwargs):
        return _ajax_success({
            'idx': 0,
            'status': 1,
            'counts': 0
        })
