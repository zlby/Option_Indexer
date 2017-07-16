# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intervals',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('lower_bound_a', models.FloatField(verbose_name='a区间下限')),
                ('upper_bound_a', models.FloatField(verbose_name='a区间上限')),
                ('lower_bound_b', models.FloatField(verbose_name='b区间下限')),
                ('upper_bound_b', models.FloatField(verbose_name='b区间上限')),
                ('lower_bound_c', models.FloatField(verbose_name='c区间下限')),
                ('upper_bound_c', models.FloatField(verbose_name='c区间上限')),
                ('negative_option', models.ForeignKey(verbose_name='反向期权', related_name='negative_intervals', to='option.Option')),
                ('positive_option', models.ForeignKey(verbose_name='正向期权', related_name='positive_intervals', to='option.Option')),
            ],
        ),
    ]
