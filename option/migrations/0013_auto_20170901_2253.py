# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-01 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0012_auto_20170821_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='future',
            name='deposit_today',
            field=models.FloatField(null=True, verbose_name='今日保证金'),
        ),
        migrations.AddField(
            model_name='option',
            name='deposit_today',
            field=models.FloatField(null=True, verbose_name='今日保证金'),
        ),
    ]