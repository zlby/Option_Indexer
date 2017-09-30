# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime, date

# Create your models here.


class Future(models.Model):
    code = models.CharField(verbose_name=u'期货代码', max_length=20, primary_key=True)
    delivery_day = models.DateField(verbose_name=u'交割日', null=True)
    deposit_today = models.FloatField(verbose_name=u'今日保证金', null=True)

    def __str__(self):
        return self.code

    @staticmethod
    def get_future_list():
        result = []
        for future in Future.objects.filter(delivery_day__gte=date.today()):
            result.append(future.code)
        return result

    @staticmethod
    def get_future_and_delivery_day_list():
        result = []
        for future in Future.objects.filter(delivery_day__gte=date.today()):
            item = {
                'code': future.code,
                'delivery_day': future.delivery_day.strftime('%Y-%m-%d'),
            }
            result.append(item)
        return result

    @staticmethod
    def get_future_option_list():
        result = []
        for future in Future.objects.filter(delivery_day__gte=date.today()):
            item = {
                'code': future.code,
                'options': Option.get_option_list(future)
            }
            result.append(item)
        return result

    def get_minute_treading_data(self, start_time, end_time=None):
        time_filter = models.Q(time__gte=start_time)
        if end_time:
            time_filter &= models.Q(time__lte=end_time)
        result = {
            'future': {
                'code': self.code,
                'data': list(treading.get_detail() for treading in
                             FutureTreadingData.objects.filter(time_filter & models.Q(future=self)))
            },
            'options': []
        }
        for option in Option.objects.filter(asset=self):
            option_data = option.get_minute_treading_data(start_time, end_time)
            if option_data:
                result['options'].append(option_data)
        return result

    def get_hour_treading_data(self, start_time, end_time=None):
        time_filter = models.Q(time__gte=start_time)
        if end_time:
            time_filter &= models.Q(time__lte=end_time)
        result = {
            'future': {
                'code': self.code,
                'data': list(treading.get_detail() for treading in
                             HourFutureTreadingData.objects.filter(time_filter & models.Q(future=self)))
            },
            'options': []
        }
        for option in Option.objects.filter(asset=self):
            option_data = option.get_hour_treading_data(start_time, end_time)
            if option_data:
                result['options'].append(option_data)
        return result

    def get_day_treading_data(self, start_time, end_time=None):
        time_filter = models.Q(time__gte=start_time)
        if end_time:
            time_filter &= models.Q(time__lte=end_time)
        result = {
            'future': {
                'code': self.code,
                'data': list(treading.get_detail() for treading in
                             DayFutureTreadingData.objects.filter(time_filter & models.Q(future=self)))
            },
            'options': []
        }
        for option in Option.objects.filter(asset=self):
            option_data = option.get_day_treading_data(start_time, end_time)
            if option_data:
                result['options'].append(option_data)
        return result


class Option(models.Model):
    code = models.CharField(verbose_name=u'期权代码', max_length=20, primary_key=True)
    asset = models.ForeignKey(verbose_name=u'标的期货', to=Future)
    deposit_today = models.FloatField(verbose_name=u'今日保证金', null=True)

    def __str__(self):
        return self.code

    @staticmethod
    def get_option_list(future):
        result = []
        for option in Option.objects.filter(asset=future):
            result.append(option.code)
        return result

    def get_minute_treading_data(self, start_time, end_time=None):
        time_filter = models.Q(time__gte=start_time)
        if end_time:
            time_filter &= models.Q(time__lte=end_time)
        all_treading_data = OptionTreadingData.objects.filter(time_filter & models.Q(option=self))
        if len(all_treading_data) > 1000:
            result = {
                'code': self.code,
                'data': list(treading.get_detail() for treading in all_treading_data)
            }
            return result
        else:
            return None

    def get_hour_treading_data(self, start_time, end_time=None):
        time_filter = models.Q(time__gte=start_time)
        if end_time:
            time_filter &= models.Q(time__lte=end_time)
        all_treading_data = HourOptionTreadingData.objects.filter(time_filter & models.Q(option=self))
        if len(all_treading_data) > 40:
            result = {
                'code': self.code,
                'data': list(treading.get_detail() for treading in all_treading_data)
            }
            return result
        else:
            return None

    def get_day_treading_data(self, start_time, end_time=None):
        time_filter = models.Q(time__gte=start_time)
        if end_time:
            time_filter &= models.Q(time__lte=end_time)
        all_treading_data = DayOptionTreadingData.objects.filter(time_filter & models.Q(option=self))
        if len(all_treading_data) > 3:
            result = {
                'code': self.code,
                'data': list(treading.get_detail() for treading in all_treading_data)
            }
            return result
        else:
            return None


class TreadingDataBase(models.Model):
    time = models.DateTimeField(verbose_name=u'时间', db_index=True)
    open_price = models.FloatField(verbose_name=u'开盘价', default=0)
    max_price = models.FloatField(verbose_name=u'最高价', default=0)
    min_price = models.FloatField(verbose_name=u'最低价', default=0)
    close_price = models.FloatField(verbose_name=u'收盘价', default=0)

    class Meta:
        abstract = True
        ordering = ['time']

    def get_detail(self):
        result = {
            'time': self.time.strftime('%Y-%m-%d %H:%M:%S'),
            'open_price': self.open_price,
            'max_price': self.max_price,
            'min_price': self.min_price,
            'close_price': self.close_price,
        }
        return result


class FutureTreadingDataBase(TreadingDataBase):
    future = models.ForeignKey(verbose_name=u'对应期货', to=Future)

    class Meta(TreadingDataBase.Meta):
        abstract = True


class FutureTreadingData(FutureTreadingDataBase):
    pass


class HourFutureTreadingData(FutureTreadingDataBase):
    pass


class DayFutureTreadingData(FutureTreadingDataBase):
    pass


class OptionTreadingDataBase(TreadingDataBase):
    option = models.ForeignKey(verbose_name=u'对应期权', to=Option)
    volatility = models.FloatField(verbose_name=u'隐含波动率', null=True)
    volume = models.FloatField(verbose_name=u'成交量', default=0)

    class Meta(TreadingDataBase.Meta):
        abstract = True

    def get_detail(self):
        result = {
            'volatility': self.volatility,
            'volume': self.volume,
        }
        result.update(super(OptionTreadingDataBase, self).get_detail())
        return result


class OptionTreadingData(OptionTreadingDataBase):
    pass


class HourOptionTreadingData(OptionTreadingDataBase):
    pass


class DayOptionTreadingData(OptionTreadingDataBase):
    pass


class Intervals(models.Model):
    positive_option = models.ForeignKey(to=Option, verbose_name='正向期权', related_name='positive_intervals')
    negative_option = models.ForeignKey(to=Option, verbose_name='反向期权', related_name='negative_intervals')
    lower_bound_a = models.FloatField(verbose_name='a区间下限', null=True)
    upper_bound_a = models.FloatField(verbose_name='a区间上限', null=True)
    lower_bound_b = models.FloatField(verbose_name='b区间下限', null=True)
    upper_bound_b = models.FloatField(verbose_name='b区间上限', null=True)
    lower_bound_c = models.FloatField(verbose_name='c区间下限', null=True)
    upper_bound_c = models.FloatField(verbose_name='c区间上限', null=True)
    rate = models.FloatField(verbose_name='买卖比例', default=1)
    current_state = models.CharField(verbose_name='当前处于的区间', null=True, max_length=5)

    def make_tread(self, positive=True):
        if positive:
            for subscribe_record in self.subscribe_set.all().select_related('client'):
                subscribe_record.client.create_notification(buy_option=self.positive_option,
                                                            sell_option=self.negative_option,
                                                            buy_lot=1,
                                                            sell_lot=self.rate)
        else:
            for subscribe_record in self.subscribe_set.all().select_related('client'):
                subscribe_record.client.create_notification(buy_option=self.negative_option,
                                                            sell_option=self.positive_option,
                                                            buy_lot=self.rate,
                                                            sell_lot=1)

    @staticmethod
    def get_possible_combo(option_code):
        possible_list = list(Intervals.objects.filter(positive_option_id=option_code)
                             .values_list('negative_option_id', flat=True))
        possible_list += list(Intervals.objects.filter(negative_option_id=option_code)
                              .values_list('positive_option_id', flat=True))
        return possible_list


class News(models.Model):
    title = models.CharField(verbose_name='标题', max_length=50)
    content = models.TextField(verbose_name='内容')
    time = models.DateTimeField(verbose_name='新闻发布时间')
    items_per_page = 4

    class Meta:
        ordering = ['-time']

    def get_detail(self):
        result = {
            'title': self.title,
            'content': self.content,
            'time': self.time.strftime('%Y-%m-%d %H:%M'),
        }
        return result

    @staticmethod
    def get_news(page_number=1):
        if page_number <= 0:
            page_number = 1
        total_page = int((News.objects.all().count() - 1) / News.items_per_page) + 1
        if page_number > total_page:
            page_number = total_page
        newses = []
        for news in News.objects.all()[News.items_per_page*(page_number-1): News.items_per_page*page_number]:
            newses.append(news.get_detail())
        return newses, total_page


class Spot(models.Model):
    time = models.DateTimeField(verbose_name=u'时间', db_index=True)
    price = models.FloatField(verbose_name=u'价格', default=0)


class Crop(models.Model):
    time = models.DateTimeField(verbose_name=u'时间')
    type = models.CharField(verbose_name=u'种类', max_length=20)
    price = models.FloatField(verbose_name=u'价格')


class ContinuousDayFutureTreadingData(TreadingDataBase):
    type = models.CharField(verbose_name=u'种类', max_length=20, default='')
