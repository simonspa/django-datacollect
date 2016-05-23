# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-23 18:35
from __future__ import unicode_literals

from django.db import migrations, models
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0030_auto_20160523_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='concern_expressed',
            field=models.CharField(choices=[('PM', 'Protection measures'), ('II', 'Independent investigation'), ('PI', 'Provide information'), ('PV', 'Concern: Pattern of violation'), ('CV', 'Concern over violation')], max_length=2, verbose_name='Concern expressed / demand'),
        ),
        migrations.AlterField(
            model_name='record',
            name='date_government_action',
            field=models.DateField(blank=True, null=True, verbose_name='Date of government action according to reply'),
        ),
        migrations.AlterField(
            model_name='record',
            name='date_govreply',
            field=models.DateField(blank=True, null=True, verbose_name='Date of government reply'),
        ),
        migrations.AlterField(
            model_name='record',
            name='further_comments',
            field=models.TextField(blank=True, verbose_name='Further comments'),
        ),
        migrations.AlterField(
            model_name='record',
            name='government_reply_action',
            field=models.CharField(choices=[('protect', 'Protection measures granted'), ('release', 'Individual released'), ('improve', 'Improved prison conditions'), ('investigate', 'Investigation opened'), ('prosecuted', 'Perpetrator suspended/prosecuted'), ('issued', 'Travel documents issued')], max_length=11, verbose_name='Government action taken accroding to reply'),
        ),
        migrations.AlterField(
            model_name='record',
            name='government_reply_content',
            field=models.CharField(choices=[('reject', 'Violation rejected'), ('incomp', 'Reponsive but incomplete'), ('immat', 'Immaterial response'), ('react', 'Steps taken to address')], max_length=6, verbose_name='Content of government reply'),
        ),
        migrations.AlterField(
            model_name='record',
            name='violations',
            field=select_multiple_field.models.SelectMultipleField(choices=[('AD', 'Arrest/Detention'), ('P', 'Prosecution'), ('UT', 'Unfair trial'), ('C', 'Conviction'), ('K', 'Killing'), ('KA', 'Killing attempt/Assault'), ('DI', 'Diappearance/Incommunicado'), ('PC', 'Held in poor conditions'), ('RT', 'Risk of torture'), ('TI', 'Torture/Ill-treatment'), ('T', 'Threats'), ('DC', 'Defamation campaign'), ('DP', 'Disciplinary proceedings'), ('S', 'Surveillance'), ('R', 'Office/home raided'), ('B', 'Barred from travelling'), ('AH', 'Administrative harassment'), ('?', 'N/A')], default='?', max_choices=3, max_length=15, verbose_name='Violation(s)'),
        ),
    ]
