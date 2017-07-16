# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('option', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('email', models.CharField(max_length=50, verbose_name='通知邮箱', null=True)),
                ('phone', models.CharField(max_length=20, verbose_name='通知手机号', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationHistory',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True, verbose_name='提醒发送时间')),
                ('buy_lot', models.IntegerField(verbose_name='买入手数')),
                ('sell_lot', models.IntegerField(verbose_name='卖出手数')),
                ('buy_option', models.ForeignKey(related_name='buy_notification', to='option.Option', verbose_name='买入期权')),
                ('client', models.ForeignKey(to='client.Client')),
                ('sell_option', models.ForeignKey(related_name='sell_notification', to='option.Option', verbose_name='卖出期权')),
            ],
        ),
        migrations.CreateModel(
            name='OptionCombo',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('client', models.ForeignKey(to='client.Client')),
                ('negative_option', models.ForeignKey(related_name='negative_clients', to='option.Option', verbose_name='反向期权')),
                ('positive_option', models.ForeignKey(related_name='positive_clients', to='option.Option', verbose_name='正向期权')),
            ],
        ),
    ]
