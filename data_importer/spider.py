# -*- coding: utf-8 -*-
# 2017.7.11 by Joey
from datetime import datetime
from queue import Queue

import requests
from bs4 import BeautifulSoup

from algorithm.others.vol_update import cal_vol_direct
from option.models import Future, FutureTreadingData, Option, OptionTreadingData, Intervals


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


class Spider(object):
    future_url = "http://www.dce.com.cn/webquote/futures_quote.jsp?varietyid=m"
    future_list_url = 'http://www.dce.com.cn/webquote/option_quote.jsp?varietyid=m'
    option_list_url = 'http://www.dce.com.cn/webquote/option_quote.jsp?varietyid=m&contractid=%s'
    queue = Queue()

    @staticmethod
    def get_all_data():
        options_data = {}
        response = requests.get(Spider.future_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", "dataT")
        rows = table.find_all('tr')
        current_time_without_second = get_current_time_without_second()
        # 因为第一行是表格标题
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
            future_data = {
                'code': future.code,
                'delivery_day': datetime.strptime(future.delivery_day.strftime('%Y-%m-%d'), '%Y-%m-%d'),
                'close_price': treading_data.close_price,
            }
            options_data.update(Spider.get_option_data(future_data))
        # scipy 不是线程安全的，但是默认会自动多线程
        # 所以取消手动多线程
        for combo in Intervals.objects.all():
            positive_option_data = options_data[combo.positive_option_id]
            negative_option_data = options_data[combo.negative_option_id]
            interval = positive_option_data['volatility'] - negative_option_data['volatility']
            if combo.lower_bound_a < interval < combo.upper_bound_a:
                if combo.current_state != 'a':
                    combo.current_state = 'a'
                    combo.save()
                    if interval > 0:
                        combo.make_tread(positive=True)
                    else:
                        combo.make_tread(positive=False)
            elif combo.lower_bound_b < interval < combo.upper_bound_b:
                if combo.current_state != 'b':
                    combo.current_state = 'b'
                    combo.save()
            elif combo.lower_bound_c < interval < combo.upper_bound_c:
                if combo.current_state != 'c':
                    combo.current_state = 'c'
                    combo.save()
                    if interval > 0:
                        combo.make_tread(positive=False)
                    else:
                        combo.make_tread(positive=True)
            else:
                # supposed tobe error
                if combo.current_state:
                    combo.current_state = None
                    combo.save()

    @staticmethod
    def get_option_data(future_data):
        future_code = future_data['code']
        response = requests.get(Spider.option_list_url % future_code)
        if response.status_code != 200:
            return {}
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", "dataT")
        rows = table.find_all("tr")
        current_time_without_second = get_current_time_without_second()
        options_data = {}
        for i in range(1, len(rows)):
            column = rows[i].find_all("td")
            option_code = future_code + '-c-' + column[15].string.strip()
            option, if_create = Option.objects.get_or_create(code=option_code, asset_id=future_code)
            last_treading_data = OptionTreadingData.objects.filter(option=option).last()
            treading_data, if_create = OptionTreadingData.objects.get_or_create(option=option,
                                                                                time=current_time_without_second)
            treading_data.open_price = clean_data(column[6].string.strip(), last_treading_data)
            treading_data.max_price = clean_data(column[5].string.strip(), last_treading_data)
            treading_data.min_price = clean_data(column[4].string.strip(), last_treading_data)
            treading_data.close_price = clean_data(column[14].string.strip(), last_treading_data)
            treading_data.volume = clean_data(column[8].string.strip(), last_treading_data, attr='volume')

            # 计算隐含波动率
            treading_data.volatility = cal_vol_direct(option_code, treading_data.close_price,
                                                      future_data['close_price'], future_data['delivery_day'])
            treading_data.save()
            option_data = {
                'code': option_code,
                'volatility': treading_data.volatility,
            }
            options_data[option_data['code']] = option_data
        return options_data


