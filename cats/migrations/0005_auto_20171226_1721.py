# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0004_auto_20171226_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewlog',
            name='last_view',
            field=models.DateTimeField(db_index=True),
        ),
    ]
