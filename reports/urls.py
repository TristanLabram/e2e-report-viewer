from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('<int:pk>/view/', views.report_view, name='report_view'),
    path('<int:pk>/toggle/', views.report_toggle_status, name='report_toggle_status'),
    path('sync/', views.sync_reports, name='sync_reports')
]
