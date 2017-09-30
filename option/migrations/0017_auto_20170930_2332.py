# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-30 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0016_remove_continuousfuture_delivery_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='continuousdayfuturetreadingdata',
            name='future',
        ),
        migrations.AddField(
            model_name='continuousdayfuturetreadingdata',
            name='type',
            field=models.CharField(default='', max_length=20, verbose_name='种类'),
        ),
        migrations.DeleteModel(
            name='ContinuousFuture',
        ),
    ]