# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0019_auto_20160523_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='violation_against_family_member',
            field=models.IntegerField(choices=[(0, 'Only HDR'), (1, 'against relative'), (2, 'against both')], default=0),
        ),
    ]
