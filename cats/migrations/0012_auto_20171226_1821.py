# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 10:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cats', '0011_auto_20171226_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatImgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adate', models.DateTimeField(auto_now_add=True)),
                ('img_hash', models.CharField(default='', max_length=64, unique=True)),
                ('img_src', models.CharField(default='', max_length=255)),
                ('img_desc', models.CharField(default='', max_length=255)),
                ('img_from', models.CharField(default='', max_length=255)),
                ('img_status', models.BooleanField(db_index=True, default=0)),
                ('img_like', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'cat imgs',
                'verbose_name_plural': 'cat imgs',
                'db_table': 'cat_imgs',
            },
        ),
        migrations.CreateModel(
            name='PicComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adate', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('content', models.TextField(default='')),
                ('stars', models.DecimalField(decimal_places=1, default=0, max_digits=4)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, to_field='username')),
                ('img_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cats.CatImgs')),
            ],
            options={
                'verbose_name': 'pic comments',
                'verbose_name_plural': 'cat imgs comments',
                'db_table': 'cats_pic_comments',
            },
        ),
        migrations.CreateModel(
            name='PicLikes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adate', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('is_like', models.IntegerField(choices=[(-1, '不喜欢'), (0, '取消'), (1, '喜欢')])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, to_field='username')),
                ('img_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cats.CatImgs')),
            ],
            options={
                'verbose_name': 'cat imgs likes',
                'verbose_name_plural': 'cat imgs likes',
                'db_table': 'cats_pic_likes',
            },
        ),
        migrations.CreateModel(
            name='PicStars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.BigIntegerField(default=0)),
                ('comments', models.BigIntegerField(default=0)),
                ('img_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cats.CatImgs')),
            ],
            options={
                'verbose_name': 'cat imgs stars',
                'verbose_name_plural': 'cat imgs stars',
                'db_table': 'cats_pic_stars',
            },
        ),
        migrations.AlterField(
            model_name='viewlog',
            name='author',
            field=models.ForeignKey(db_column='author', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]