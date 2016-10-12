# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-12 14:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0061_auto_20161006_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherrecord',
            name='case_type',
            field=models.IntegerField(choices=[(0, 'NGO/Trade union/...'), (1, 'NHRI'), (2, 'Statement by official'), (3, 'Law/bill'), (4, 'Mass violation/pattern'), (5, 'Anonymous cases'), (6, 'PR on individual'), (7, 'Country visit by SR')], default=0, verbose_name='Type of case'),
        ),
    ]
