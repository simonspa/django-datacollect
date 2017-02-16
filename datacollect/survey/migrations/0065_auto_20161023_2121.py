# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-23 19:21
from __future__ import unicode_literals

from django.db import migrations, models
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0064_auto_20161015_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='govreply_content',
            field=models.CharField(blank=True, choices=[('reject', 'Violation rejected'), ('incomp', 'Reponsive but incomplete'), ('immat', 'Immaterial response'), ('react', 'Steps taken to address'), ('transl', 'In translation'), ('na', 'N/A')], help_text='According to rating criteria by Piccone (2012)', max_length=6, verbose_name='Content of government reply'),
        ),
        migrations.AlterField(
            model_name='record',
            name='perpetrator',
            field=select_multiple_field.models.SelectMultipleField(choices=[('U', 'Unknown'), ('P', 'Police/security forces'), ('CS', 'Public official/administration/judiciary'), ('A', 'Army'), ('AO', 'Armed opposition'), ('B', 'Business/landholder'), ('M', 'Mob'), ('PM', 'Paramilitary group'), ('PP', 'Private person'), ('RA', 'Religious authority')], default='U', help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=10, verbose_name='Alleged perpetrator'),
        ),
        migrations.AlterField(
            model_name='record',
            name='perpetrator2',
            field=select_multiple_field.models.SelectMultipleField(blank=True, choices=[('U', 'Unknown'), ('P', 'Police/security forces'), ('CS', 'Public official/administration/judiciary'), ('A', 'Army'), ('AO', 'Armed opposition'), ('B', 'Business/landholder'), ('M', 'Mob'), ('PM', 'Paramilitary group'), ('PP', 'Private person'), ('RA', 'Religious authority')], help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=10, verbose_name='Alleged perpetrator #2'),
        ),
        migrations.AlterField(
            model_name='record',
            name='perpetrator3',
            field=select_multiple_field.models.SelectMultipleField(blank=True, choices=[('U', 'Unknown'), ('P', 'Police/security forces'), ('CS', 'Public official/administration/judiciary'), ('A', 'Army'), ('AO', 'Armed opposition'), ('B', 'Business/landholder'), ('M', 'Mob'), ('PM', 'Paramilitary group'), ('PP', 'Private person'), ('RA', 'Religious authority')], help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=10, verbose_name='Alleged perpetrator #3'),
        ),
    ]