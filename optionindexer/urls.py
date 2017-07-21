from django.conf.urls import include, url
from django.contrib import admin
import optionindexer.views as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'optionindexer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index),
    # url(r'^doc$', views.doc),
    url(r'^client/', include('client.urls')),
    url(r'^market/', include('option.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
