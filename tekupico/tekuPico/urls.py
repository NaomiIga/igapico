"""tekuPico URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import include, url
admin.autodiscover()
from django.conf import settings
from cms import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^',include('django.contrib.staticfiles.urls')),
    url(r'^post_test', views.post_test, name="post_test"),
    url(r'^pico_login', views.pico_login, name="pico_login"),
    url(r'^shoplog', views.shoplog, name="shoplog"),
    url(r'^shop_loading', views.shop_loading, name="shop_loading"),
    url(r'^hint', views.hint, name="hint"),
    url(r'^first', views.first, name="first"),
    url(r'^treasure_check', views.treasure_check, name="treasure_check"),
    url(r'^export_csv', views.export_csv, name="export_csv"),
    url(r'^map', views.map, name="map"),
    url(r'^finish', views.finish, name="finish"),
    url(r'^key_get', views.key_get, name="key_get")
]
