# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 09:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0009_viewlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewlog',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', related_query_name='author', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
