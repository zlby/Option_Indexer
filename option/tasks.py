from __future__ import absolute_import, unicode_literals
from celery import task
from data_importer.spider import Spider
from data_importer.news_spider import NewsSpider
from data_importer.for_all_products_price import daily_update
from data_importer.for_caution_money import update_deposit

@task
def news_spider():
    NewsSpider.get_data()


@task
def option_spider():
    Spider.get_all_data()


@task
def all_products_price_spider():
    daily_update()


@task
def caution_money_spider():
    update_deposit()