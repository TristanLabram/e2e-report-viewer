import os
from datetime import datetime
from django.conf import settings
from .models import Report

# Scans the test_report directory for any new test reports, adding these to the DB 
def scan_reports():
    # Properties
    root = settings.REPORT_STORAGE_ROOT
    discovered = 0

    #Loop through all the date directories in the report root directory
    for date_dir in sorted(os.listdir(root)):
        date_path = os.path.join(root, date_dir)
        
        #Ignore any files placed in the report root, there shouldn't be any
        if not os.path.isdir(date_path):
            continue

        try:
            report_date = datetime.strptime(date_dir, '%Y-%m-%d').date()
        except ValueError:
            continue #skip any directory that isn't a YYYY-MM-DD folder

        #Loop through files within the current date directory
        for filename in sorted(os.listdir(date_path)):
            if not filename.endswith('.html'):
                continue #Skip any non html file
            
            #Store the relative path so the DB is portable
            relative_path = os.path.join(date_dir, filename)

            # Get_or_create returns a tuple of (report, bool) and we only want the bool, so the `_` tells
            # python to ignore the returned Report. This saves new reports to the DB or returns existing ones
            _, created = Report.objects.get_or_create(
                filepath=relative_path,
                defaults={
                    'report_date': report_date,
                    'filename': filename,
                    'status': 'c',
                },
            )
            if created:
                discovered += 1
    # After loop, return the number of new reports found and added to the DB
    return discovered