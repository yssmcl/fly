from django.conf.urls import url

from . import views

app_name = 'docente'
urlpatterns = [
    url(r'^novo/$', views.NovoDocente.as_view(), name='novo'),
    url(r'^consulta/$', views.ConsultaDocente.as_view(), name='consulta'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetalheDocente.as_view(), name='detalhe'),
]
