from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F
from django.contrib.auth import views as auth_views
from django.views import View, generic

class LoginView(auth_views.LoginView):
	template_name = 'accounts/login.html'
