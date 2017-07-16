# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


class Future(models.Model):
    code = models.CharField(verbose_name=u'期货代码', max_length=20, primary_key=True)
    delivery_day = models.DateField(verbose_name=u'交割日', null=True)


class Option(models.Model):
    code = models.CharField(verbose_name=u'期权代码', max_length=20, primary_key=True)
    asset = models.ForeignKey(verbose_name=u'标的期货', to=Future)


class TreadingDataBase(models.Model):
    time = models.DateTimeField(verbose_name=u'时间', db_index=True)
    open_price = models.FloatField(verbose_name=u'开盘价', default=0)
    max_price = models.FloatField(verbose_name=u'最高价', default=0)
    min_price = models.FloatField(verbose_name=u'最低价', default=0)
    close_price = models.FloatField(verbose_name=u'收盘价', default=0)

    class Meta:
        abstract = True


class FutureTreadingData(TreadingDataBase):
    future = models.ForeignKey(verbose_name=u'对应期货', to=Future)


class OptionTreadingData(TreadingDataBase):
    option = models.ForeignKey(verbose_name=u'对应期权', to=Option)
    volatility = models.FloatField(verbose_name=u'隐含波动率', null=True)
    volume = models.FloatField(verbose_name=u'成交量', default=0)


class Intervals(models.Model):
    positive_option = models.ForeignKey(to=Option, verbose_name='正向期权', related_name='positive_intervals')
    negative_option = models.ForeignKey(to=Option, verbose_name='反向期权', related_name='negative_intervals')
    lower_bound_a = models.FloatField(verbose_name='a区间下限')
    upper_bound_a = models.FloatField(verbose_name='a区间上限')
    lower_bound_b = models.FloatField(verbose_name='b区间下限')
    upper_bound_b = models.FloatField(verbose_name='b区间上限')
    lower_bound_c = models.FloatField(verbose_name='c区间下限')
    upper_bound_c = models.FloatField(verbose_name='c区间上限')

