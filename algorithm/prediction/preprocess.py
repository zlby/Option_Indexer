from algorithm.data_provider.data_provider_django import *
from option.models import *
import datetime

def data_preprocess(code:str, end_day:datetime.date, days:int):

    start_day = end_day - datetime.timedelta(days=days)
    query_set = FutureTreadingData.objects.filter(future=code).filter(time__gt=start_day).filter(time__lt=end_day).order_by('time')
    time_list = []
    close_price = 0
    open_price = 0
    max_price_list = []
    min_price_list = []
    blurry_data_list = []

    # for i in range(days):

