from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^consultar/$', views.consultar, name='consultar'),
    url(r'^consultarlink/(?P<palabra>\d+)/$', views.consultarlink, name='consultarlink'),
]