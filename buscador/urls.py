from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^consultar/$', views.consultar, name='consultar'),
    url(r'^detalle/$', views.detalle, name='detalle'),
    #url(r'^consultarlink/(?P<palabra>\d+)/$', views.consultarlink, name='consultarlink'),
]