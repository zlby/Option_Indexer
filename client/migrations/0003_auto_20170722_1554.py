# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0010_intervals_current_state'),
        ('client', '0002_auto_20170722_1426'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='optioncombo',
            name='negative_option',
        ),
        migrations.RemoveField(
            model_name='optioncombo',
            name='positive_option',
        ),
        migrations.AddField(
            model_name='optioncombo',
            name='combo_interval',
            field=models.ForeignKey(related_name='subscribe_set', to='option.Intervals', null=True),
        ),
    ]
