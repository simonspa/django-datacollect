# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-24 16:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0015_auto_20170324_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followup',
            name='attention',
            field=models.IntegerField(choices=[(1, 'For sure'), (2, 'Probably'), (3, 'Rather not'), (4, 'Definitely not'), (6, "I don't know")], default=6, null=True, verbose_name='Attention impact'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='case',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='followup', serialize=False, to='survey.Record', verbose_name='Case'),
        ),
        migrations.AlterField(
            model_name='followup',
            name='unique_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Unique ID'),
        ),
    ]
