# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-20 20:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0008_auto_20170320_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followup',
            name='attention',
        ),
        migrations.RemoveField(
            model_name='followup',
            name='rating',
        ),
    ]