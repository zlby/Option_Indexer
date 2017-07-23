# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0009_intervals_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervals',
            name='current_state',
            field=models.CharField(max_length=5, null=True, verbose_name='当前处于的区间'),
        ),
    ]
