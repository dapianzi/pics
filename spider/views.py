from django.shortcuts import render
from django.views.generic import TemplateView,View
from django.db.models import ObjectDoesNotExist

from pics.utils import _ajax_error,_ajax_success,_is_doubtful
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
        keyword = request.GET.get('keyword', '')
        type_id = request.GET.get('type', 0)
        if len(keyword) >= 2:
            context['keyword'] = keyword
            context['type_id'] = type_id
            self.ip = request.META.get("REMOTE_ADDR", '')
            if not self._is_blocked():
                # todo SPIDER TASK STATUS
                # spider_task = spider_models.SpiderTask.objects.filter(keyword=keyword, content_type=type_id)
                # if spider_task[0].status == 1:
                #     pass
                # elif spider_task[0].status == 2:
                #     pass
                # else:
                #     # launch a task
                #     spider_models.SpiderTask()

                self._recordSearch(keyword)
            else:
                context['result'] = {
                    'count': 0,
                    'status': 1,
                    'current': 0,
                }
        elif keyword != '':
            context['err_msg'] = '搜索关键词不能少于2个字哦'

        return render(
            request, self.template_name, context
        )

    @property
    def _doubtful_count(self):
        return 20

    def _is_blocked(self):
        try:
            block = spider_models.BlackList.objects.get(ip=self.ip)
        except ObjectDoesNotExist:
            return False
        else:
            return True

    def _recordSearch(self, content):
        doubtful = _is_doubtful(content)
        spider_models.SearchRecord.objects.create(ip=self.ip, content=content, is_doubtful=doubtful)
        # consider to block ip
        if spider_models.SearchRecord.objects.filter(ip=self.ip, is_doubtful=True).count() >= self._doubtful_count:
            spider_models.BlackList.objects.create(ip=self.ip)


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
