from ast import Pass
from django import template
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from . import views

# Account urls
urlpatterns = [
    path(
        'login/',
        LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        'profile/',
        views.profile_view,
        name="profile",
    ),
    path(
        'profile/password/',
        PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            success_url="/profile/",
        ),
        name="password_change",
    ),
]
