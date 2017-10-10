from __future__ import absolute_import, unicode_literals
from celery import task
from data_importer.spider import Spider
from data_importer.news_spider import NewsSpider
from data_importer.for_all_products_price import daily_update
from data_importer.for_caution_money import update_deposit
from datetime import datetime, timedelta

from option.models import FutureTreadingData, HourFutureTreadingData, DayFutureTreadingData


@task
def news_spider():
    NewsSpider.get_data()


@task
def option_spider():
    Spider.get_all_data()


@task
def option_hour_data_turner():
    hour_pre = (datetime.now()+timedelta(hours=-1))
    hour_pre += timedelta(minutes=-hour_pre.minute, seconds=-hour_pre.second, microseconds=-hour_pre.microsecond)
    hour_next = hour_pre+timedelta(hours=1)

    option_data = FutureTreadingData.objects.filter(time__gt=hour_pre, time__lt=hour_next)
    future = option_data.first().future
    open_price = option_data.first().open_price
    max_price = 0
    min_price = 99999
    close_price = option_data.last().close_price
    for option in option_data:
        if option.max_price > max_price:
            max_price = option.max_price
        if option.min_price < min_price:
            min_price = option.min_price

    new_option_hour_data = HourFutureTreadingData(time=hour_pre,
                                                  open_price=open_price,
                                                  max_price=max_price,
                                                  min_price=min_price,
                                                  close_price=close_price,
                                                  future=future)
    new_option_hour_data.save()


@task
def option_day_data_turner():
    day_pre = (datetime.now()+timedelta(days=-1))
    day_pre += timedelta(hours=-day_pre.hour,
                         minutes=-day_pre.minute,
                         seconds=-day_pre.second,
                         microseconds=-day_pre.microsecond)
    day_next = day_pre+timedelta(days=1)
    option_data = HourFutureTreadingData.objects.filter(time__gt=day_pre, time__lt=day_next)
    future = option_data.first().future
    open_price = option_data.first().open_price
    max_price = 0
    min_price = 99999
    close_price = option_data.last().close_price
    for option in option_data:
        if option.max_price > max_price:
            max_price = option.max_price
        if option.min_price < min_price:
            min_price = option.min_price

    new_option_day_data = DayFutureTreadingData(time=day_pre,
                                                open_price=open_price,
                                                max_price=max_price,
                                                min_price=min_price,
                                                close_price=close_price,
                                                future=future)
    new_option_day_data.save()


@task
def all_products_price_spider():
    daily_update()


@task
def caution_money_spider():
    update_deposit()