from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    #Add account URLs
    path('accounts/', include('accounts.urls')),

    #Add report URLs (placeholder for now)
    #path("reports/", include("reports.urls")),

    #Root URL to redirect to the report list (or login if unauthenticated)
    # WIP setting this to redirect to login until the reports app is made
    path('', lambda request: redirect('login')),
]
