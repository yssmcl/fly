from django.conf.urls import url

from . import views

app_name = 'curso_extensao'
urlpatterns = [
	url(r'^novo/$', views.NovoCursoExtensao.as_view(), name='novo'),
	url(r'^consulta/$', views.ConsultaCursoExtensao.as_view(), name='consulta'),
	url(r'^(?P<pk>[0-9]+)/$', views.DetalheCursoExtensao.as_view(), name='detalhe'),
	url(r'^(?P<pk>[0-9]+)/pdf/$', views.GeracaoPDFCursoExtensao.as_view(), name='pdf'),
]
