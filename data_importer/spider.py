# -*- coding: utf-8 -*-
# 2017.7.11 by Joey
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from option.models import *


def clean_data(current_data, last_treading_data, attr='close_price'):
    if current_data != u'--':
        return float(current_data)
    else:
        if last_treading_data:
            return getattr(last_treading_data, attr)
        else:
            return 0


def get_current_time_without_second():
    current_time = datetime.now()
    # 去掉秒的数据，实现分钟数据的获取
    return datetime(current_time.year, current_time.month, current_time.day,
                    current_time.hour, current_time.minute, second=0)


class FutureSpider(object):
    url = "http://www.dce.com.cn/webquote/futures_quote.jsp?varietyid=m"

    @staticmethod
    def get_data():
        response = requests.get(FutureSpider.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", "dataT")
        rows = table.find_all('tr')
        # 因为第一行是表格标题
        current_time_without_second = get_current_time_without_second()
        for i in range(1, len(rows)):
            columns = rows[i].find_all('td')
            name = columns[0].string.strip()
            future, if_create = Future.objects.get_or_create(code=name)
            last_treading_data = FutureTreadingData.objects.filter(future=future).last()
            treading_data, if_create = FutureTreadingData.objects.get_or_create(future=future,
                                                                                time=current_time_without_second)
            treading_data.open_price = clean_data(columns[1].string.strip(), last_treading_data)
            treading_data.max_price = clean_data(columns[2].string.strip(), last_treading_data)
            treading_data.min_price = clean_data(columns[3].string.strip(), last_treading_data)
            # 这里是最新价代替收盘价
            treading_data.close_price = clean_data(columns[4].string.strip(), last_treading_data)
            treading_data.save()


class OptionSpider(object):
    future_list_url = 'http://www.dce.com.cn/webquote/option_quote.jsp?varietyid=m'
    option_list_url = 'http://www.dce.com.cn/webquote/option_quote.jsp?varietyid=m&contractid=%s'

    @staticmethod
    def get_data():
        # 先找到所有的豆粕期货
        response = requests.get(OptionSpider.future_list_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        drop_down_list = soup.find(id='contractselect')
        items = drop_down_list.find_all("option")
        futures = []
        for item in items:
            futures.append(item.text)
        # 再对每个期货分别找到他们的所有期权数据
        for future_code in futures:
            future, if_create = Future.objects.get_or_create(code=future_code)
            response = requests.get(OptionSpider.option_list_url % future_code)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find("table", "dataT")
            rows = table.find_all("tr")
            current_time_without_second = get_current_time_without_second()
            for i in range(1, len(rows)):
                column = rows[i].find_all("td")
                option_code = future_code + '-c-' + column[15].string.strip()
                option, if_create = Option.objects.get_or_create(code=option_code, asset=future)
                last_treading_data = OptionTreadingData.objects.filter(option=option).last()
                treading_data, if_create = OptionTreadingData.objects.get_or_create(option=option,
                                                                                    time=current_time_without_second)
                treading_data.open_price = clean_data(column[6].string.strip(), last_treading_data)
                treading_data.max_price = clean_data(column[5].string.strip(), last_treading_data)
                treading_data.min_price = clean_data(column[4].string.strip(), last_treading_data)
                treading_data.close_price = clean_data(column[14].string.strip(), last_treading_data)
                treading_data.volume = clean_data(column[8].string.strip(), last_treading_data, 'volume')
                treading_data.save()


