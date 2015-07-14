from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^buscador/$', views.buscador),
    url(r'^consultar/$', views.consultar, name='consultar'),
]