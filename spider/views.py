# coding=utf-8
import os
import time

from django.shortcuts import render
from django.views.generic import View
from django.db.models import ObjectDoesNotExist

from pics.utils import _ajax_error, _ajax_success, _is_doubtful
from . import models as spider_models


# Create your views here.


class IndexView(View):
    """
    首页搜索
    """
    template_name = 'spider/index.html'
    ip = ''

    @property
    def _DOUBTFUL_COUNT(self):
        return 20
    @property
    def _MAX_TASKS(self):
        return 16
    @property
    def _TASK_STATUS_EXPIRED(self):
        return 3
    @property
    def _TASK_STATUS_CACHING(self):
        return 2
    @property
    def _TASK_STATUS_RUNNING(self):
        return 1
    @property
    def _TASK_STATUS_PENDING(self):
        return 0

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
                # if tasks number more than _MAX_TASKS, raise too busy error
                running_tasks = spider_models.SpiderTask.objects.filter(
                    status__lt=self._TASK_STATUS_CACHING
                ).count()
                if running_tasks >= self._MAX_TASKS:
                    # too busy
                    context['is_busy'] = True
                    return render(request, self.template_name, context)

                is_new_task = False
                spider_task = spider_models.SpiderTask.objects.filter(
                    keyword=keyword, content_type=type_id).order_by('-id')[:1]
                # todo SPIDER TASK STATUS
                if spider_task and spider_task[0].status:
                    # already exist a task
                    if spider_task[0].status <= self._TASK_STATUS_RUNNING:
                        pass
                    elif spider_task[0].status == self._TASK_STATUS_CACHING:
                        pass
                    else:
                        pass
                else:
                    is_new_task = True
                if is_new_task:
                    # launch a task
                    self.launch_task(keyword, type_id)
                self._recordSearch(keyword)
            else:
                context['result'] = {
                    'count': 0,
                    'status': 1,
                    'current': 0,
                }
        elif keyword != '':
            context['err_msg'] = '搜索关键词不能少于2个字哦'

        return render(request, self.template_name, context)

    def _launch_task(self, keyword, content_type):
        st = spider_models.SpiderTask.objects.create(
            keyword=keyword, content_type=content_type, status=self._TASK_STATUS_PENDING,
            run_time=time.time()
        )
        if st:
            spiders = spider_models.Spider.objects.filter(content_type=content_type)
            if spiders:
                for s in spiders:
                    os.popen('/var/www/shell/run_scrapy.sh %s -a str=%s -a task_id=%s' % (s.name, keyword, s.id))

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
        if spider_models.SearchRecord.objects.filter(ip=self.ip, is_doubtful=True).count() >= self._DOUBTFUL_COUNT:
            spider_models.BlackList.objects.create(ip=self.ip)


class GetItem(View):
    """
    拉取结果
    """

    def post(self, request, *args, **kwargs):
        keyword = request.POST.get('keyword', '')
        type_id = request.POST.get('type', 0)

        return _ajax_success({
            'idx': 0,
            'status': 1,
            'counts': 0
        })


def handle_process(request):
    # task_id = request.POST.get('id', 0)
    pass