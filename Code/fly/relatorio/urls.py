from django.conf.urls import url

from . import views

app_name = 'relatorio'
urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/novo/$', views.NovoRelatorio.as_view(), name='novo'),
    # url(r'^lista/(?P<pk>[0-9]+)/$', views.ListaRelatorio.as_view(), name='lista'),
    # url(r'^consulta/(?P<pk>[0-9]+)/$', views.DetalheRelatorio.as_view(), name='detalhe'),
]
