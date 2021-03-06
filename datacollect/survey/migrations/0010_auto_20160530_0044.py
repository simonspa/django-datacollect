# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 22:44
from __future__ import unicode_literals

from django.db import migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0009_auto_20160529_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='perpetrator',
            field=select_multiple_field.models.SelectMultipleField(choices=[('?', 'N/A'), ('P', 'Police/security forces'), ('CS', 'Civil servant/administration/judiciary'), ('A', 'Army'), ('AO', 'Armed opposition'), ('B', 'Business/landholder'), ('M', 'Mob'), ('U', 'Unknown')], default='?', help_text='Select maximum 2 items with <i>Ctrl+Click</i>', max_choices=2, max_length=10, verbose_name='Alleged perpetrator'),
        ),
    ]
