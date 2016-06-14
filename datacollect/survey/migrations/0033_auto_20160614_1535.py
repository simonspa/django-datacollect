# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-14 13:35
from __future__ import unicode_literals

from django.db import migrations
import select_multiple_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0032_auto_20160612_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='violations',
            field=select_multiple_field.models.SelectMultipleField(choices=[('?', 'N/A'), ('AD', 'Arrest/Detention'), ('IC', ' + Incommunicado'), ('PC', ' + Held in poor conditions'), ('RT', ' + Risk of torture'), ('TI', 'Torture/Ill-treatment'), ('ED', 'Enforced disappearance'), ('KA', 'Physical attack'), ('KK', ' + Killing attempt'), ('K', '  + Killing'), ('DI', 'Kidnapping'), ('P', 'Prosecution'), ('UT', ' + Unfair trial'), ('C', ' + Conviction'), ('T', 'Threats'), ('S', 'Surveillance'), ('R', 'Office/home raided'), ('DC', 'Defamation campaign'), ('DP', 'Disciplinary proceedings'), ('B', 'Travel restrictions'), ('AH', 'Administrative harassment'), ('FI', 'Failure to intervene/protect')], default='?', help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=50, verbose_name='Violation(s)'),
        ),
        migrations.AlterField(
            model_name='record',
            name='violations2',
            field=select_multiple_field.models.SelectMultipleField(blank=True, choices=[('?', 'N/A'), ('AD', 'Arrest/Detention'), ('IC', ' + Incommunicado'), ('PC', ' + Held in poor conditions'), ('RT', ' + Risk of torture'), ('TI', 'Torture/Ill-treatment'), ('ED', 'Enforced disappearance'), ('KA', 'Physical attack'), ('KK', ' + Killing attempt'), ('K', '  + Killing'), ('DI', 'Kidnapping'), ('P', 'Prosecution'), ('UT', ' + Unfair trial'), ('C', ' + Conviction'), ('T', 'Threats'), ('S', 'Surveillance'), ('R', 'Office/home raided'), ('DC', 'Defamation campaign'), ('DP', 'Disciplinary proceedings'), ('B', 'Travel restrictions'), ('AH', 'Administrative harassment'), ('FI', 'Failure to intervene/protect')], default='?', help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=50, verbose_name='Violation(s) #2'),
        ),
        migrations.AlterField(
            model_name='record',
            name='violations3',
            field=select_multiple_field.models.SelectMultipleField(blank=True, choices=[('?', 'N/A'), ('AD', 'Arrest/Detention'), ('IC', ' + Incommunicado'), ('PC', ' + Held in poor conditions'), ('RT', ' + Risk of torture'), ('TI', 'Torture/Ill-treatment'), ('ED', 'Enforced disappearance'), ('KA', 'Physical attack'), ('KK', ' + Killing attempt'), ('K', '  + Killing'), ('DI', 'Kidnapping'), ('P', 'Prosecution'), ('UT', ' + Unfair trial'), ('C', ' + Conviction'), ('T', 'Threats'), ('S', 'Surveillance'), ('R', 'Office/home raided'), ('DC', 'Defamation campaign'), ('DP', 'Disciplinary proceedings'), ('B', 'Travel restrictions'), ('AH', 'Administrative harassment'), ('FI', 'Failure to intervene/protect')], default='?', help_text='Select multiple items with <i>Ctrl+Click</i>', max_length=50, verbose_name='Violation(s) #3'),
        ),
    ]
