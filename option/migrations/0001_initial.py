# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Future',
            fields=[
                ('code', models.CharField(max_length=20, serialize=False, verbose_name='\u671f\u8d27\u4ee3\u7801', primary_key=True)),
                ('delivery_day', models.DateField(null=True, verbose_name='\u4ea4\u5272\u65e5')),
            ],
        ),
        migrations.CreateModel(
            name='FutureTreadingData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(verbose_name='\u65f6\u95f4', db_index=True)),
                ('open_price', models.FloatField(default=0, verbose_name='\u5f00\u76d8\u4ef7')),
                ('max_price', models.FloatField(default=0, verbose_name='\u6700\u9ad8\u4ef7')),
                ('min_price', models.FloatField(default=0, verbose_name='\u6700\u4f4e\u4ef7')),
                ('close_price', models.FloatField(default=0, verbose_name='\u6536\u76d8\u4ef7')),
                ('future', models.ForeignKey(verbose_name='\u5bf9\u5e94\u671f\u8d27', to='option.Future')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('code', models.CharField(max_length=20, serialize=False, verbose_name='\u671f\u6743\u4ee3\u7801', primary_key=True)),
                ('asset', models.ForeignKey(verbose_name='\u6807\u7684\u671f\u8d27', to='option.Future')),
            ],
        ),
        migrations.CreateModel(
            name='OptionTreadingData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(verbose_name='\u65f6\u95f4', db_index=True)),
                ('open_price', models.FloatField(default=0, verbose_name='\u5f00\u76d8\u4ef7')),
                ('max_price', models.FloatField(default=0, verbose_name='\u6700\u9ad8\u4ef7')),
                ('min_price', models.FloatField(default=0, verbose_name='\u6700\u4f4e\u4ef7')),
                ('close_price', models.FloatField(default=0, verbose_name='\u6536\u76d8\u4ef7')),
                ('volatility', models.FloatField(null=True, verbose_name='\u9690\u542b\u6ce2\u52a8\u7387')),
                ('volume', models.FloatField(default=0, verbose_name='\u6210\u4ea4\u91cf')),
                ('option', models.ForeignKey(verbose_name='\u5bf9\u5e94\u671f\u6743', to='option.Option')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
