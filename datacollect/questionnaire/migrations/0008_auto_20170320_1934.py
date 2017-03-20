# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-20 18:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0007_auto_20170319_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='incident_date_1',
            field=models.DateField(blank=True, help_text='Format YYY-MM-DD', null=True, verbose_name='Date of the incident'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='incident_date_2',
            field=models.DateField(blank=True, help_text='Format YYY-MM-DD', null=True, verbose_name='Date of the incident'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='incident_date_3',
            field=models.DateField(blank=True, help_text='Format YYY-MM-DD', null=True, verbose_name='Date of the incident'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='incident_date_4',
            field=models.DateField(blank=True, help_text='Format YYY-MM-DD', null=True, verbose_name='Date of the incident'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='incident_date_5',
            field=models.DateField(blank=True, help_text='Format YYY-MM-DD', null=True, verbose_name='Date of the incident'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='incident_text_1',
            field=models.TextField(blank=True, verbose_name='Brief description of the incident'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='incident_text_2',
            field=models.TextField(blank=True, verbose_name='Brief description of the incident'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='incident_text_3',
            field=models.TextField(blank=True, verbose_name='Brief description of the incident'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='incident_text_4',
            field=models.TextField(blank=True, verbose_name='Brief description of the incident'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='incident_text_5',
            field=models.TextField(blank=True, verbose_name='Brief description of the incident'),
        ),
    ]
