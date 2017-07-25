from django.conf.urls import url

from . import views

app_name = 'parecer'
urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/novo/$', views.NovoParecer.as_view(), name='novo'),
    url(r'^(?P<pk>[0-9]+)/consulta/$', views.ConsultaParecer.as_view(), name='consulta'),
    url(r'^detalhe/(?P<pk>[0-9]+)/$', views.DetalheParecer.as_view(), name='detalhe'),
	url(r'^deletar/$', views.DeletarParecer.as_view(), name='deletar'),
]
