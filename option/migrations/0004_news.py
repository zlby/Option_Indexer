# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0003_auto_20170716_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=20, verbose_name='标题')),
                ('content', models.TextField(verbose_name='内容')),
                ('time', models.DateTimeField(verbose_name='新闻发布时间')),
            ],
        ),
    ]
