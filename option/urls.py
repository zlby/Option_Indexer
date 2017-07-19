# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import option.views as views

urlpatterns = [
    url(r'^futures/$', views.get_future_list),
    url(r'^future/(\w+)/options/$', views.get_option_list),
    url(r'^news/$', views.get_news),
]