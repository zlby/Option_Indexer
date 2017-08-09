# -*- coding: utf-8 -*-
from django.conf.urls import include, url
import client.views as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'huaqi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.get_client_info),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.new_client),
    url(r'^set_new_password/$', views.set_new_password),
    url(r'^set_new_email_or_phone/$', views.set_new_email_phone),
    url(r'^get_all_combo/$', views.get_all_combo),
    url(r'^get_all_notification/$', views.get_all_notification),
    url(r'^notification/(\d+)/read/$', views.mark_notification_as_read),
    url(r'^delete_combo/$', views.delete_combo),
    url(r'^add_combo/$', views.new_combo),
]