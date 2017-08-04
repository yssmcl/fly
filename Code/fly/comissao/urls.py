from django.conf.urls import url

from . import views

app_name = 'comissao'
urlpatterns = [
    url(r'^nova/$', views.NovaComissao.as_view(), name='novo'),
    url(r'^consulta/$', views.ConsultaComissao.as_view(), name='consulta'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetalheComissao.as_view(), name='detalhe'),
]
