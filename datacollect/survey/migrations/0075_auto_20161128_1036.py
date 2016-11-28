# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-28 09:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0074_auto_20161128_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='date_govreply_further',
            field=models.CharField(blank=True, max_length=500, verbose_name='Date(s) of further replies'),
        ),
        migrations.AddField(
            model_name='record',
            name='date_incident_unspecific',
            field=models.CharField(blank=True, max_length=500, verbose_name='If unspecific'),
        ),
        migrations.AddField(
            model_name='record',
            name='is_released',
            field=models.BooleanField(default=False, verbose_name='If arrested: released?'),
        ),
        migrations.AddField(
            model_name='record',
            name='violation_family_who',
            field=models.CharField(blank=True, max_length=500, verbose_name='Concerned family member'),
        ),
    ]
