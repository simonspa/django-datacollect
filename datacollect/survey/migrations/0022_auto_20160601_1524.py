# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-01 13:24
from __future__ import unicode_literals

from django.db import migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0021_auto_20160601_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='joint_with',
            field=select_multiple_field.models.SelectMultipleField(blank=True, choices=[('FrASSEM', 'FrASSEM'), ('FrEXPRESS', 'FrEXPRESS'), ('TORTURE', 'TORTURE'), ('WGAD', 'WGAD'), ('WGED', 'WGED'), ('SumEXECU', 'SumEXECU'), ('WOMEN', 'WOMEN'), ('FrRELIGION', 'FrRELIGION'), ('JUDGES', 'JUDGES'), ('INDIGENOUS', 'INDIGENOUS'), ('TERRORISM', 'TERRORISM'), ('BUSINESS', 'BUSINESS'), ('HEALTH', 'HEALTH'), ('ENVIR', 'ENVIR'), ('FOOD', 'FOOD')], help_text='Select any number items with <i>Ctrl+Click</i>', max_length=200),
        ),
    ]
