# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0029_auto_20160612_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='date_govaction',
            field=models.DateField(blank=True, help_text='Format YYY-MM-DD', null=True, verbose_name='Date of action according to reply'),
        ),
        migrations.AlterField(
            model_name='record',
            name='govreply_action',
            field=models.CharField(blank=True, choices=[('protect', 'Protection measures granted'), ('release', 'Individual released early'), ('improve', 'Improved prison conditions'), ('investigate', 'Investigation opened'), ('prosecuted', 'Perpetrator suspended/prosecuted'), ('issued', 'Travel documents issued')], max_length=11, verbose_name='Action taken according to reply'),
        ),
    ]