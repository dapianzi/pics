# coding=utf-8
import os
import time
import json

from django.shortcuts import render, get_object_or_404
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

    _DOUBTFUL_COUNT = 50
    _MAX_TASKS = 16
    _MAX_RUNTIME = 1
    _TASK_STATUS_EXPIRED = 3
    _TASK_STATUS_CACHING = 2
    _TASK_STATUS_RUNNING = 1
    _TASK_STATUS_PENDING = 0

    def get(self, request, *args, **kwargs):
        context = dict()
        context['title'] = 'What can I do for you?'
        context['types'] = spider_models.ContentType.objects.filter(active=spider_models.ContentType.ACTIVE[0][0])
        keyword = request.GET.get('keyword', '')
        type_id = request.GET.get('type', 0)
        if len(keyword) >= 2:
            context['keyword'] = keyword
            context['type_id'] = type_id
            self.ip = request.META.get("REMOTE_ADDR", '')
            if not self._is_blocked():
                # if tasks number more than _MAX_TASKS, raise too busy error
                running_tasks = self._running_scrapy()
                if running_tasks >= self._MAX_TASKS:
                    # too busy
                    context['is_busy'] = True
                    return render(request, self.template_name, context)
                # handle search task
                context['get_result'] = json.dumps(self._handle_search_task(keyword, type_id))
                self._recordSearch(keyword)
            else:
                context['get_result'] = False
        elif keyword != '':
            context['get_result'] = False
            context['err_msg'] = '搜索关键词不能少于2个字哦'

        return render(request, self.template_name, context)

    def _handle_search_task(self, keyword, type_id):
        content_type = get_object_or_404(spider_models.ContentType, id=type_id)
        spider_task = spider_models.SpiderTask.objects.filter(
            keyword=keyword, content_type=content_type).order_by('-id')[:1]
        if spider_task.count() > 0:
            renew_task = False
            # if run_time is empty
            if spider_task[0].run_time is None:
                renew_task = True
            # if pending, running
            elif spider_task[0].status == self._TASK_STATUS_PENDING or spider_task[0].status == self._TASK_STATUS_RUNNING:
                running_timestamp = time.mktime(spider_task[0].run_time.timetuple())
                running_expired = time.time() - self._MAX_RUNTIME*86400
                if running_timestamp <= running_expired:
                    renew_task = True
            # if caching
            elif spider_task[0].status == self._TASK_STATUS_CACHING:
                running_timestamp = time.mktime(spider_task[0].run_time.timetuple())
                running_expired = time.time() - content_type.expire_time * 86400
                if running_timestamp <= running_expired:
                    renew_task = True
            else:
                renew_task = True

            if renew_task:
                st = spider_task[0]
                st.status = self._TASK_STATUS_EXPIRED
                st.save()
                # launch a task
                return self._launch_task(keyword, content_type)
        else:
            return self._launch_task(keyword, content_type)

    def _launch_task(self, keyword, content_type):
        st = spider_models.SpiderTask.objects.create(
            keyword=keyword, content_type=content_type, status=self._TASK_STATUS_PENDING,
            run_time=time.time()
        )
        ret = []
        if st:
            spiders = spider_models.Spider.objects.filter(content_type=content_type)
            if spiders:
                for s in spiders:
                    # os.popen('/var/www/shell/run_scrapy.sh %s -a str=%s -a task_id=%s' % (s.name, keyword, s.id))
                    f = os.popen('python -V')
                    ret.append(f.read())
        print(ret)
        return ret

    def _running_scrapy(self):
        with os.popen('ps -ef | grep "scrapy crawl" | grep -v "grep" | wc -l') as f:
            return f.read()
        return self._MAX_TASKS

    def _is_blocked(self):
        try:
            block = spider_models.BlackList.objects.get(ip=self.ip, is_deny=1)
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

class GetResult(View):
    """
    拉取结果
    """

    def post(self, request, *args, **kwargs):
        keyword = request.POST.get('keyword', '')
        type_id = request.POST.get('type', 0)

        content_type = get_object_or_404(spider_models.ContentType, id=type_id)
        task = get_object_or_404(spider_models.SpiderTask, keyword=keyword,
                                 content_type=content_type).order_by('-id')[:1]
        results = spider_models.Items.objects.filter(spider_info=task)

        return _ajax_success({
            'idx': 0,
            'status': 1,
            'counts': 0,
            'result': results
        })

def handle_process(request):
    # task_id = request.POST.get('id', 0)
    pass