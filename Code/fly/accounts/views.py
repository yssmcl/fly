from django.contrib.auth import views as auth_views

class LoginView(auth_views.LoginView):
	pass

class LogoutView(auth_views.LogoutView):
	pass
