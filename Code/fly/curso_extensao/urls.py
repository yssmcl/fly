from django.conf.urls import url

from . import views

app_name = 'curso_extensao'
urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^novo_curso_extensao/$', views.NovoCursoExtensao.as_view(), name='novo_curso_extensao')
]