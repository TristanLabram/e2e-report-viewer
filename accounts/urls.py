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
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
]
