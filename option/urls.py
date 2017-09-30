# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import option.views as views

urlpatterns = [
    url(r'^futures/$', views.get_future_list),
    url(r'^future/(\w+)/options/$', views.get_option_list),
    url(r'^future/(\w+)/treading/$', views.get_future_treading_data),
    url(r'^option/(\w+)/possible_combo/$', views.get_possible_combo),
    url(r'^options/treading_data', views.get_option_treading_data),
    url(r'^asset_evaluation/$', views.get_asset_evaluation),
    url(r'^hedging/$', views.get_hedging),
    url(r'^choose_future/$', views.choose_future),
    url(r'^cross_breed_hedge/$', views.get_cross_breed_hedge),
    url(r'^distribution/$', views.get_distribution),
    url(r'^future_time/$', views.get_future_delivery_day_list),
    url(r'^news/$', views.get_news),
    url(r'^distributions/$', views.get_distribution)
]