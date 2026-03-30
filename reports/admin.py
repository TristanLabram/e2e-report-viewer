from django.contrib import admin
from .models import Report

#Enable inspection of reports via Django admin page
@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'filename', 'status', 'discovered_at')
    list_filter = ('status', 'report_date')
    search_fields = ('filename',)