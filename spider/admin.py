from django.contrib import admin
from django.http import HttpResponse, StreamingHttpResponse
from django.core import serializers
from spider.models import Spider, ContentType, SpiderTask, BlackList
# Register your models here.

@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    # 列表项
    list_display = ['name', 'max_item', 'expire_time', 'active']
    # 批量操作
    actions = [
        'set_active',
        'set_discard',
        'export_csv',
    ]

    def set_active(self, request, queryset):
        r = queryset.update(active=0)
        self.message_user(request, "%s个类别被激活" % r)
    # 设置操作描述
    set_active.short_description = '激活'
    def set_discard(self, req, qys):
        r = qys.update(active=1)
        self.message_user(req, "%s个类别被激活" % r)
    set_discard.short_description = '禁用'
    def export_csv(self, request, queryset):
        """导出csv"""
        response = StreamingHttpResponse('\n'.join([','.join(
            # list元素转str
            list(map(lambda x: str(x), x))
        ) for x in list(
            # queryset 转 list
            queryset.values_list('name', 'max_item', 'expire_time', 'active')
        )]).encode('gbk').decode('gbk'), charset='gbk', content_type='attachment/csv')
        response['Content-Disposition'] = 'attachment;filename="test.csv"'
        return response
    export_csv.short_description = '导出csv'

@admin.register(Spider)
class SpiderAdmin(admin.ModelAdmin):
    list_display = ('name', 'c_name', 'domain', 'n_start', 'n_end', 'content_type')

@admin.register(SpiderTask)
class SpiderTaskAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'content_type', 'status', 'run_time', 'finish_time', 'running')

@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ('ip', 'time', 'is_deny')
