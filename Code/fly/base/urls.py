from django.conf.urls import url

from . import views

app_name = 'curso_extensao'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^novo/$', views.NovoCursoExtensao.as_view(), name='novo'),
	url(r'^consulta/$', views.ConsultaCursoExtensao.as_view(), name='consulta'),
	url(r'^(?P<pk>[0-9]+)/$', views.DetalheCursoExtensao.as_view(), name='detalhe'),
]