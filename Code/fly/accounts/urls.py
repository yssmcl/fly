from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
	url(r'^login/$', views.LoginView.as_view(), name='login')
]