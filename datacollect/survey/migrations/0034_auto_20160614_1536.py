# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-14 13:36
from __future__ import unicode_literals

from django.db import migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0033_auto_20160614_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='perpetrator',
            field=select_multiple_field.models.SelectMultipleField(choices=[('P', 'Police/security forces'), ('CS', 'Public official/administration/judiciary'), ('A', 'Army'), ('AO', 'Armed opposition'), ('B', 'Business/landholder'), ('M', 'Mob'), ('U', 'Unknown')], default='U', help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=10, verbose_name='Alleged perpetrator'),
        ),
        migrations.AlterField(
            model_name='record',
            name='perpetrator2',
            field=select_multiple_field.models.SelectMultipleField(blank=True, choices=[('P', 'Police/security forces'), ('CS', 'Public official/administration/judiciary'), ('A', 'Army'), ('AO', 'Armed opposition'), ('B', 'Business/landholder'), ('M', 'Mob'), ('U', 'Unknown')], default='U', help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=10, verbose_name='Alleged perpetrator #2'),
        ),
        migrations.AlterField(
            model_name='record',
            name='perpetrator3',
            field=select_multiple_field.models.SelectMultipleField(blank=True, choices=[('P', 'Police/security forces'), ('CS', 'Public official/administration/judiciary'), ('A', 'Army'), ('AO', 'Armed opposition'), ('B', 'Business/landholder'), ('M', 'Mob'), ('U', 'Unknown')], default='U', help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=10, verbose_name='Alleged perpetrator #3'),
        ),
    ]