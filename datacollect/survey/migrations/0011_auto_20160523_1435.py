# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 14:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_record_followup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='followup',
            new_name='follow_up_case',
        ),
        migrations.RenameField(
            model_name='record',
            old_name='intl_coop',
            new_name='international_cooperation',
        ),
    ]
