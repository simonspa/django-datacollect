# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0025_auto_20160523_1507'),
    ]

    operations = [
        migrations.RenameField(
            model_name='record',
            old_name='notes',
            new_name='further_comments',
        ),
        migrations.AddField(
            model_name='record',
            name='date_government_action',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='date_government_reply',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='government_reply_action',
            field=models.CharField(choices=[('protect', 'Protection measures granted'), ('release', 'Individual released'), ('improve', 'Improved prison conditions'), ('investigate', 'Investigation opened'), ('prosecuted', 'Perpetrator suspended/prosecuted'), ('issued', 'Travel documents issued')], default='reject', max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='government_reply_content',
            field=models.CharField(choices=[('reject', 'Violation rejected'), ('incomp', 'Reponsive but incomplete'), ('immat', 'Immaterial response'), ('react', 'Steps taken to address')], default='protect', max_length=6),
            preserve_default=False,
        ),
    ]
