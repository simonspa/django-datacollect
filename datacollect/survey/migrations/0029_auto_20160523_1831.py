# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0028_auto_20160523_1828'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='date_government_reply',
        ),
        migrations.AddField(
            model_name='record',
            name='date_govreply',
            field=models.DateField(blank=True, null=True, verbose_name='Date of the government reply'),
        ),
        migrations.AlterField(
            model_name='record',
            name='date_intervention',
            field=models.DateField(blank=True, null=True, verbose_name='Date of the intervention'),
        ),
        migrations.AlterField(
            model_name='record',
            name='type_intervention',
            field=models.CharField(choices=[('UA', 'UA'), ('JUA', 'JUA'), ('AL', 'AL'), ('JAL', 'JAL'), ('PR', 'PR')], max_length=3, verbose_name='Type of intervention'),
        ),
    ]
