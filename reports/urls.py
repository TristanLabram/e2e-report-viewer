from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    #Sprint 4 urls
    path('<int:pk>/view/', views.report_view, name='report_view'),
    path('<int:pk>/toggle/', views.report_toggle_status, name='report_toggle_status'),
]
