# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-07 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0068_auto_20161107_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='business_case',
            field=models.BooleanField(default=False, verbose_name='Business-related case'),
        ),
        migrations.AddField(
            model_name='record',
            name='business_company',
            field=models.CharField(blank=True, max_length=500, verbose_name='Name of company'),
        ),
    ]
