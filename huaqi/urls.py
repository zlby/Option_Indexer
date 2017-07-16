from django.conf.urls import include, url
from django.contrib import admin
import huaqi.views as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'huaqi.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index),
    url(r'^doc$', views.doc),
    url(r'^client/', include('client.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
