# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import option.views as views

urlpatterns = [
    url(r'^futures/$', views.get_future_list),
    url(r'^future/(\w+)/options/$', views.get_option_list),
    url(r'^future/(\w+)/treading/$', views.get_future_treading_data),
    url(r'^option/(\w+)/possible_combo/$', views.get_possible_combo),
    url(r'^options/treading_data', views.get_option_treading_data),
    url(r'^news/$', views.get_news),
]