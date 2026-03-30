from django.core.management.base import BaseCommand
from reports.services import scan_reports

# Management command to scan the report directory for new reports
class Command(BaseCommand):
    # Add command help text
    help = "Scan the report storage directory for new HTML reports"

    def handle(self, *args, **options):
        count = scan_reports()
        self.stdout.write(
            self.style.SUCCESS(f"Discovered {count} new report(s).")
        )