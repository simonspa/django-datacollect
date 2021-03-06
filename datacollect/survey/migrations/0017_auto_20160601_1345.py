# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 11:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0016_auto_20160531_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='person_id',
            field=models.CharField(help_text='Form YYYY-CCC-P, where YYYY is the year of publication, CCC is the paragraph number given in the report, and P the person number within the communication', max_length=11, verbose_name='Person ID'),
        ),
    ]
