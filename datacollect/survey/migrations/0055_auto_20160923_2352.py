# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-23 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0054_auto_20160923_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='otherrecord',
            name='case_type',
            field=models.IntegerField(choices=[(0, 'NGO'), (1, 'NHRI'), (2, 'Statement by official'), (3, 'Law/bill'), (4, 'Mass violation/pattern')], default=0, verbose_name='Type of case'),
        ),
        migrations.AlterField(
            model_name='otherrecord',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Subject of communication'),
        ),
    ]
