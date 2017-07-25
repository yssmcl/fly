from django.conf.urls import url

from . import views

app_name = 'relatorio'
urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/novo/$', views.NovoRelatorio.as_view(), name='novo'),
    url(r'^(?P<pk>[0-9]+)/consulta/$', views.ConsultaRelatorio.as_view(), name='consulta'),
    url(r'^detalhe/(?P<pk>[0-9]+)/$', views.DetalheRelatorio.as_view(), name='detalhe'),
    url(r'^pdf/(?P<pk>[0-9]+)/$', views.GeracaoPDFRelatorio.as_view(), name='pdf'),
	url(r'^deletar/$', views.DeletarRelatorio.as_view(), name='deletar'),
]
