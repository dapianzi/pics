from django.contrib import admin
from spider.models import Spider, ContentType, SpiderTask
# Register your models here.

admin.site.register(ContentType)
admin.site.register(Spider)
admin.site.register(SpiderTask)
