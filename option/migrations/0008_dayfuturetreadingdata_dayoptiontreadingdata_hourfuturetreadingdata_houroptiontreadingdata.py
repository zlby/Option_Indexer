# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0007_auto_20170720_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayFutureTreadingData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('time', models.DateTimeField(db_index=True, verbose_name='时间')),
                ('open_price', models.FloatField(default=0, verbose_name='开盘价')),
                ('max_price', models.FloatField(default=0, verbose_name='最高价')),
                ('min_price', models.FloatField(default=0, verbose_name='最低价')),
                ('close_price', models.FloatField(default=0, verbose_name='收盘价')),
                ('future', models.ForeignKey(to='option.Future', verbose_name='对应期货')),
            ],
            options={
                'ordering': ['time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DayOptionTreadingData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('time', models.DateTimeField(db_index=True, verbose_name='时间')),
                ('open_price', models.FloatField(default=0, verbose_name='开盘价')),
                ('max_price', models.FloatField(default=0, verbose_name='最高价')),
                ('min_price', models.FloatField(default=0, verbose_name='最低价')),
                ('close_price', models.FloatField(default=0, verbose_name='收盘价')),
                ('volatility', models.FloatField(null=True, verbose_name='隐含波动率')),
                ('volume', models.FloatField(default=0, verbose_name='成交量')),
                ('option', models.ForeignKey(to='option.Option', verbose_name='对应期权')),
            ],
            options={
                'ordering': ['time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HourFutureTreadingData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('time', models.DateTimeField(db_index=True, verbose_name='时间')),
                ('open_price', models.FloatField(default=0, verbose_name='开盘价')),
                ('max_price', models.FloatField(default=0, verbose_name='最高价')),
                ('min_price', models.FloatField(default=0, verbose_name='最低价')),
                ('close_price', models.FloatField(default=0, verbose_name='收盘价')),
                ('future', models.ForeignKey(to='option.Future', verbose_name='对应期货')),
            ],
            options={
                'ordering': ['time'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HourOptionTreadingData',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('time', models.DateTimeField(db_index=True, verbose_name='时间')),
                ('open_price', models.FloatField(default=0, verbose_name='开盘价')),
                ('max_price', models.FloatField(default=0, verbose_name='最高价')),
                ('min_price', models.FloatField(default=0, verbose_name='最低价')),
                ('close_price', models.FloatField(default=0, verbose_name='收盘价')),
                ('volatility', models.FloatField(null=True, verbose_name='隐含波动率')),
                ('volume', models.FloatField(default=0, verbose_name='成交量')),
                ('option', models.ForeignKey(to='option.Option', verbose_name='对应期权')),
            ],
            options={
                'ordering': ['time'],
                'abstract': False,
            },
        ),
    ]
