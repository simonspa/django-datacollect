# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 18:10
from __future__ import unicode_literals

from django.db import migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0022_auto_20160601_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='issue_area',
            field=select_multiple_field.models.SelectMultipleField(choices=[('?', 'N/A'), ('WR', "Women's rights"), ('CRS', "Children's rights"), ('IPR', "Indigenous peoples' rights"), ('LGBTI', 'LGBTI issues'), ('MRR', "Migrants'/refugees' rights"), ('LR', 'Labour rights'), ('POV', 'Poverty'), ('RTF', 'Right to food'), ('HI', 'Health issues'), ('HRFE', 'Housing rights/forced evictions'), ('LNR', 'Land rights/environment'), ('CR', 'Cultural rights'), ('RF', 'Religious freedom'), ('PR', "Prisoner's rights"), ('AT', 'Torture'), ('ED', 'Enforced disappearance'), ('H', 'Homocide'), ('PV', 'Police violence'), ('AC', 'Corruption'), ('DV', 'Democratic/voting rights'), ('IF', 'Internet freedom'), ('HRE', 'Human rights education'), ('TJ', 'Transitional justice')], default='?', help_text='Select maximum 2 items with <i>Ctrl+Click</i>', max_choices=2, max_length=10),
        ),
    ]
