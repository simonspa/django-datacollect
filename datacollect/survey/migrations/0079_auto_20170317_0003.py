# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-16 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0078_record_follow_ups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='follow_ups',
            field=models.ManyToManyField(blank=True, default=None, related_name='_record_follow_ups_+', to='survey.Record', verbose_name='Follow-up Person IDs'),
        ),
    ]