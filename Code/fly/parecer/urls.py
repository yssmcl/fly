from django.conf.urls import url

from . import views

app_name = 'parecer'
urlpatterns = [
	url(r'^(?P<pk>[0-9]+)/novo/$', views.NovoParecer.as_view(), name='novo'),
	url(r'^lista/(?P<pk>[0-9]+)/$', views.ListaParecer.as_view(), name='lista'),
	url(r'^consulta/(?P<pk>[0-9]+)/$', views.DetalheParecer.as_view(), name='detalhe'),
]
