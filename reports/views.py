import os
import re
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.conf import settings
from .models import Report
from .services import scan_reports

# View for the report list page
@login_required
def report_list(request):
    if request.user.is_admin:
        # Has the admin selected show all or just current?
        show_all = request.GET.get('show', 'current') == 'all'

        if show_all:
            reports = Report.objects.all()
        else:
            reports = Report.objects.filter(status='c')

    else: #Non-admins
        reports = Report.objects.filter(status='c')
        show_all = False

    # Render the page template, attaching the view model
    return render(request, 'reports/report_list.html', {
        'reports': reports,
        'show_all': show_all,
    })

# View single report, this loads the test report HTML file directly
@login_required
def report_view(request, pk):
    report = get_object_or_404(Report, pk=pk)

    # Prevent view-only users from accessing archived reports
    if report.status == 'a' and not request.user.is_admin:
        raise HttpResponseForbidden("Current user doesn't have permission to view archived reports")
    
    file_path = os.path.join(settings.REPORT_STORAGE_ROOT, report.filepath)

    if not os.path.exists(file_path):
        raise Http404('Report file not found')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    return HttpResponse(html_content, content_type='text/html')

# Toggle the status of a report between "Current" and "Archived"
@login_required
def report_toggle_status(request, pk):
    #Add protection and checks
    if request.method != 'POST':
        return redirect('report_list')
    
    if not request.user.is_admin:
        messages.error(request, "You do not have permission to change the status of reports")
        return redirect('report_list')
    
    #Get the report to be edited
    report = get_object_or_404(Report, pk=pk)

    #Toggle the status
    report.status = 'a' if report.status == 'c' else 'c'
    report.save()

    messages.success(request, f'"{report.filename}" is now {report.get_status_display()}.')

    #Preserve the current admin filter after redirect
    referer = request.META.get('HTTP_REFERER', '')
    if 'show=all' in referer:
        return redirect('/reports/?show=all') # Show all reports
    
    #The page loads in "Show current" by default
    return redirect('report_list')

# Uses the scan_reports command to check for new reports
@login_required
def sync_reports(request):
    if request.method != 'POST':
        return redirect('report_list')
    
    count = scan_reports()

    if count > 0:
        messages.success(request, f'Discovered {count} new report(s)')
    else:
        messages.info(request, "No new reports found")

    return redirect('report_list')
    