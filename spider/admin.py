from django.contrib import admin
from spider.models import Spider, ContentType, SpiderTask, BlackList
# Register your models here.

admin.site.register(ContentType)

@admin.register(Spider)
class SpiderAdmin(admin.ModelAdmin):
    list_display = ('name', 'c_name', 'domain', 'n_start', 'n_end', 'content_type')

@admin.register(SpiderTask)
class SpiderTaskAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'content_type', 'status', 'run_time', 'finish_time', 'running')

@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ('ip', 'time', 'is_deny')
