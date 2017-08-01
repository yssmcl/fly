from django.conf.urls import url

from . import views

app_name = 'relatorio'
urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/novo/$', views.NovoRelatorio.as_view(), name='novo'),
    url(r'^(?P<pk>[0-9]+)/consulta/$', views.ConsultaRelatorio.as_view(), name='consulta'),
    url(r'^detalhe/(?P<pk>[0-9]+)/$', views.DetalheRelatorio.as_view(), name='detalhe'),
    url(r'^upload/(?P<pk>[0-9]+)/$', views.UploadArquivoRelatorio.as_view(), name='upload_arquivo'),
    url(r'^arquivos/(?P<pk>[0-9]+)/$', views.ListaArquivosRelatorio.as_view(), name='lista_arquivos'),
    url(r'^download/(?P<pk>[0-9]+)/$', views.DownloadArquivoRelatorio.as_view(), name='download_arquivo'),
    url(r'^deletar_arquivo/$', views.DeletarArquivoRelatorio.as_view(), name='deletar_arquivo'),
    url(r'^pdf/(?P<pk>[0-9]+)/$', views.GeracaoPDFRelatorio.as_view(), name='pdf'),
	url(r'^deletar/$', views.DeletarRelatorio.as_view(), name='deletar'),
]
