from django.db import models
from django.contrib.auth.models import User,GroupManager

# Create your models here.
class ViewLog(models.Model):


    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # 默认为id字段，其他字段需要用'unique'索引
        to_field='username',
        db_column='author',
    )
    last_page = models.IntegerField(default=0)
    # db_index=True 建立索引
    last_view = models.DateTimeField(db_index=True)
    class Meta:
        verbose_name = 'view log'
        verbose_name_plural = 'view log'
        # 指定表名
        db_table = 'cats_view_log'

class CatImgs(models.Model):
    adate = models.DateTimeField(auto_now_add=True)
    img_hash = models.CharField(default='', null=False, max_length=64, unique=True)
    img_src = models.CharField(default='', max_length=255)
    img_desc = models.CharField(default='', max_length=255)
    img_from = models.CharField(default='', max_length=255)
    img_status = models.BooleanField(default=0, db_index=True)
    img_like = models.IntegerField(default=0)
    class Meta:
        verbose_name = 'cat imgs'
        verbose_name_plural = 'cat imgs'
        db_table = 'cat_imgs'

class PicComments(models.Model):
    adate = models.DateTimeField(db_index=True, auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        to_field='username',
        related_name='+',
    )
    img_id = models.ForeignKey(
        CatImgs,
        on_delete=models.CASCADE,
    )
    content = models.TextField(default='')
    stars = models.DecimalField(default=0, max_digits=4, decimal_places=1)
    class Meta:
        verbose_name = 'pic comments'
        verbose_name_plural = 'cat imgs comments'
        db_table = 'cats_pic_comments'

class PicLikes(models.Model):
    IS_LIKE = (
        (-1,'不喜欢'),
        (0,'取消'),
        (1,'喜欢'),
    )
    adate = models.DateTimeField(db_index=True, auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        to_field='username',
        related_name='+',
    )
    img_id = models.ForeignKey(
        CatImgs,
        on_delete=models.CASCADE,
    )
    is_like = models.IntegerField(choices=IS_LIKE)
    class Meta:
        verbose_name = 'cat imgs likes'
        verbose_name_plural = 'cat imgs likes'
        db_table = 'cats_pic_likes'

class PicStars(models.Model):
    img_id = models.ForeignKey(
        CatImgs,
        on_delete=models.CASCADE,
    )
    stars = models.BigIntegerField(default=0)
    comments = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = 'cat imgs stars'
        verbose_name_plural = 'cat imgs stars'
        db_table = 'cats_pic_stars'