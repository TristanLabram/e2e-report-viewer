from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Report

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