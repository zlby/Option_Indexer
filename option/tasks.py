from __future__ import absolute_import, unicode_literals
from celery import task
from data_importer.spider import Spider
from data_importer.news_spider import NewsSpider


@task
def news_spider():
    NewsSpider.get_data()


@task
def option_spider():
    Spider.get_all_data()