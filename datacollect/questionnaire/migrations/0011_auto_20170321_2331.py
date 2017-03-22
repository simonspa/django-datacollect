# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-21 22:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0010_auto_20170320_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='email_address',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True, verbose_name='Email address'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='further_comments',
            field=models.TextField(blank=True, verbose_name='Further comments'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='rating',
            field=models.IntegerField(choices=[(1, 'Much better'), (2, 'Somewhat better'), (3, 'Situation stayed the same overall'), (4, 'Somewhat worse'), (5, 'Much worse'), (6, "I don't know")], default=6, null=True),
        ),
    ]