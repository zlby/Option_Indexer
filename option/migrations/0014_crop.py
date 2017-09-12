# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-12 06:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0013_auto_20170901_2253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(verbose_name='时间')),
                ('type', models.CharField(max_length=20, verbose_name='种类')),
                ('price', models.FloatField(verbose_name='价格')),
            ],
        ),
    ]
