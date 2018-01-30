# coding=utf-8
from django.db import models

# Create your models here.

class Config(models.Model):
    """
    配置信息
    """
    CONF_TYPE = (
        (1, 'int'),
        (2, 'str'),
        (3, 'float'),
        (4, 'json'),
    )
    conf_key = models.CharField('配置项', max_length=50, default='', unique=True, null=False)
    conf_type = models.IntegerField('配置项', choices=CONF_TYPE)
    conf_value = models.TextField('配置项', max_length=1024, default='')
    def __str__(self):
        return self.conf_key

class Spider(models.Model):
    """
    爬虫信息配置
    """
    name = models.CharField('爬虫名称', max_length=50, default='', db_index=True)
    c_name = models.CharField('爬虫名称', max_length=50, default='')
    domain = models.CharField('爬虫域名', max_length=150, default='')
    n_start = models.IntegerField('起始页数', default=0)
    n_end = models.IntegerField('终止页数', default=0)
    content_type = models.ForeignKey(
        'ContentType',
        related_name='spider_content_type',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '%s[%s]' % (self.c_name, self.name)

class ContentType(models.Model):
    """
    抓取内容配置
    """
    ACTIVE = (
        (0, 'active'),
        (1, 'discard'),
    )
    name = models.CharField('内容类型', max_length=50, default='')
    max_item = models.IntegerField('每个爬虫最大抓取数', default=10)
    expire_time = models.IntegerField('过期时间(天)', default=30)
    active = models.BooleanField('是否废弃', choices=ACTIVE, db_index=True, default=0)

    def __str__(self):
        return self.name

class SpiderTask(models.Model):
    """
    爬虫任务
    """
    STATUS = (
        (0, '初始化'),
        (1, '抓取中'),
        (2, '缓存中'),
        (3, '已过期'),
    )
    keyword = models.CharField('爬虫关键字', max_length=50, default='', db_index=True)
    content_type = models.ForeignKey(
        ContentType,
        related_name='task_content_type',
        on_delete=models.CASCADE,
    )
    status = models.IntegerField('任务状态', choices=STATUS, default=0, db_index=True)
    run_time = models.DateTimeField('爬虫开始时间', auto_now_add=True)
    finish_time = models.DateTimeField('爬虫结束时间', null=True)
    running = models.IntegerField('运行数', default=0)

    def __str__(self):
        return self.keyword

class SpiderProcess(models.Model):
    """
    爬虫进程
    """
    spider = models.ForeignKey(
        Spider,
        related_name='spider_process_name',
        on_delete=models.CASCADE
    )

    pid = models.IntegerField('pid', null=True)

class SearchRecord(models.Model):
    """
    搜索记录
    """
    time = models.DateTimeField('搜索时间', auto_now_add=True, null=False)
    ip = models.GenericIPAddressField('客户端IP', default='', db_index=True)
    content = models.CharField('搜索内容', max_length=50)
    is_doubtful = models.BooleanField('是否可疑', default=False, db_index=True)

    def __str__(self):
        return "[%s]%s - %s" % (self.time, self.ip, self.content)

class BlackList(models.Model):
    """
    IP黑名单
    """
    IS_DENY = (
        (1, '黑名单'),
        (2, '白名单'),
    )
    time = models.DateTimeField('添加时间', auto_now_add=True, null=False)
    ip = models.GenericIPAddressField('客户端IP', default='', db_index=True)
    is_deny = models.BooleanField('黑白名单', choices=IS_DENY, default=1)
    def __str__(self):
        return self.ip

class Items(models.Model):
    """
    抓取结果
    """
    time = models.DateTimeField('抓取时间', auto_now_add=True)
    spider_info = models.ForeignKey(
        SpiderTask,
        related_name='spider_info',
        on_delete=models.CASCADE,
    )
    spider = models.ForeignKey(
        Spider,
        related_name='spider_id',
        on_delete=models.CASCADE,
    )
    result = models.TextField('抓取结果', default='', max_length=2048)
